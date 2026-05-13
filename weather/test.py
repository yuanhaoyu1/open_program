import math
import random
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import matplotlib
import platform


# 解决中文显示问题
def set_chinese_font():
    """设置中文字体，解决中文显示问题"""
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 根据操作系统设置中文字体
    system = platform.system()
    if system == 'Windows':
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    elif system == 'Darwin':  # macOS
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'SimHei', 'DejaVu Sans']
    else:  # Linux
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'DejaVu Sans']

    # 设置字体大小
    plt.rcParams['font.size'] = 12


# 调用字体设置函数
set_chinese_font()


def simulate_optimal_stopping(n, num_simulations=10000, top_percent=None):
    """
    模拟37%法则的最优停止问题

    参数:
    n: 追求者数量
    num_simulations: 模拟次数
    top_percent: 前百分之几被认为是优质追求者 (例如0.1表示前10%)

    返回:
    包含各种统计信息的字典
    """
    # 计算k值：n/e的整数部分
    k = int(n / math.e)

    # 初始化计数器
    best_chosen_count = 0
    top_percent_chosen_count = 0

    # 计算前百分之几的阈值
    if top_percent is not None:
        top_count = math.ceil(top_percent * n)
        threshold = n - top_count + 1
    else:
        threshold = None

    # 存储每次模拟的选择结果
    chosen_ranks = []

    for _ in range(num_simulations):
        # 生成追求者质量列表: 1到n，n为最佳
        candidates = list(range(1, n + 1))
        # 随机排列顺序
        random.shuffle(candidates)

        # 前k个追求者中的最佳质量
        best_in_k = max(candidates[:k]) if k > 0 else 0

        # 从第k+1个开始寻找第一个比best_in_k好的追求者
        chosen = None
        chosen_rank = None

        for i in range(k, n):
            if candidates[i] > best_in_k:
                chosen = candidates[i]
                chosen_rank = i
                break

        # 如果没有找到，选择最后一个
        if chosen is None:
            chosen = candidates[-1]
            chosen_rank = n - 1

        # 记录选择结果
        chosen_ranks.append(chosen)

        # 检查是否选中最佳（质量n）
        if chosen == n:
            best_chosen_count += 1

        # 检查是否选中前百分之几
        if threshold is not None and chosen >= threshold:
            top_percent_chosen_count += 1

    # 计算概率
    best_prob = best_chosen_count / num_simulations
    top_percent_prob = top_percent_chosen_count / num_simulations if top_percent is not None else None

    # 计算选择质量的分布
    rank_counts = defaultdict(int)
    for rank in chosen_ranks:
        rank_counts[rank] += 1

    # 返回结果
    result = {
        'n': n,
        'k': k,
        'num_simulations': num_simulations,
        'best_prob': best_prob,
        'best_count': best_chosen_count,
        'chosen_ranks': chosen_ranks,
        'rank_counts': rank_counts
    }

    if top_percent is not None:
        result.update({
            'top_percent': top_percent,
            'threshold': threshold,
            'top_percent_prob': top_percent_prob,
            'top_percent_count': top_percent_chosen_count
        })

    return result


def run_simulations(n_values, num_simulations=10000, top_percent=0.1):
    """
    对多个n值运行模拟

    参数:
    n_values: n值列表
    num_simulations: 每个n的模拟次数
    top_percent: 前百分之几被认为是优质追求者

    返回:
    包含所有模拟结果的字典
    """
    results = {}

    for n in n_values:
        print(f"正在模拟 n={n}...")
        results[n] = simulate_optimal_stopping(n, num_simulations, top_percent)

    return results


def plot_results(results):
    """
    绘制模拟结果的可视化图表
    """
    # 提取数据
    n_values = sorted(results.keys())
    best_probs = [results[n]['best_prob'] for n in n_values]
    top_percent_probs = [results[n]['top_percent_prob'] for n in n_values]

    # 创建图表
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # 图1: 选中最佳追求者的概率
    axes[0, 0].plot(n_values, best_probs, 'bo-', linewidth=2, markersize=6)
    axes[0, 0].axhline(y=1 / math.e, color='r', linestyle='--', label=f'理论极限 (1/e ≈ {1 / math.e:.3f})')
    axes[0, 0].set_xlabel('追求者数量 (n)')
    axes[0, 0].set_ylabel('选中最佳追求者的概率')
    axes[0, 0].set_title('37%法则: 选中最佳追求者的概率')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()

    # 图2: 选中前10%追求者的概率
    top_percent_value = results[n_values[0]]["top_percent"] * 100
    axes[0, 1].plot(n_values, top_percent_probs, 'go-', linewidth=2, markersize=6)
    axes[0, 1].axhline(y=results[n_values[0]]["top_percent"], color='r', linestyle='--',
                       label=f'盲选概率 ({top_percent_value}%)')
    axes[0, 1].set_xlabel('追求者数量 (n)')
    axes[0, 1].set_ylabel(f'选中前{top_percent_value:.0f}%追求者的概率')
    axes[0, 1].set_title(f'37%法则: 选中前{top_percent_value:.0f}%追求者的概率')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()

    # 图3: 选择质量分布 (以n=30为例)
    if 30 in results:
        n = 30
        rank_counts = results[n]['rank_counts']
        ranks = list(range(1, n + 1))
        counts = [rank_counts.get(rank, 0) for rank in ranks]
        probabilities = [count / results[n]['num_simulations'] for count in counts]

        axes[1, 0].bar(ranks, probabilities, alpha=0.7)
        if 'threshold' in results[n]:
            axes[1, 0].axvline(x=results[n]['threshold'], color='r', linestyle='--',
                               label=f'前{results[n]["top_percent"] * 100:.0f}%阈值')
        axes[1, 0].set_xlabel('追求者质量排名')
        axes[1, 0].set_ylabel('被选中的概率')
        axes[1, 0].set_title(f'追求者质量分布 (n={n})')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend()

    # 图4: 37%法则与盲选概率对比
    blind_probs = [1 / n for n in n_values]
    axes[1, 1].plot(n_values, best_probs, 'bo-', linewidth=2, markersize=6, label='37%法则')
    axes[1, 1].plot(n_values, blind_probs, 'ro-', linewidth=2, markersize=6, label='盲选')
    axes[1, 1].set_xlabel('追求者数量 (n)')
    axes[1, 1].set_ylabel('选中最佳追求者的概率')
    axes[1, 1].set_title('37%法则 vs 盲选: 选中最佳追求者的概率')
    axes[1, 1].set_yscale('log')  # 使用对数刻度更清晰地显示差异
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend()

    plt.tight_layout()
    plt.show()

    return fig


def print_detailed_results(results):
    """
    打印详细的模拟结果
    """
    print("=" * 80)
    print("37%法则模拟结果汇总")
    print("=" * 80)

    for n in sorted(results.keys()):
        result = results[n]
        print(f"\n追求者数量 n = {n}")
        print(f"- 最优k值: {result['k']} (约{result['k'] / n * 100:.1f}%)")
        print(f"- 模拟次数: {result['num_simulations']:,}")
        print(f"- 选中最佳追求者的概率: {result['best_prob']:.4f} ({result['best_prob'] * 100:.2f}%)")

        if 'top_percent' in result:
            print(f"- 前{result['top_percent'] * 100:.0f}%阈值质量值: >= {result['threshold']}")
            print(
                f"- 选中前{result['top_percent'] * 100:.0f}%追求者的概率: {result['top_percent_prob']:.4f} ({result['top_percent_prob'] * 100:.2f}%)")

        # 盲选概率对比
        blind_prob = 1 / n
        improvement = result['best_prob'] / blind_prob
        print(f"- 盲选概率: {blind_prob:.4f} ({blind_prob * 100:.2f}%)")
        print(f"- 37%法则相对于盲选的提升倍数: {improvement:.2f}x")


# 主程序
if __name__ == "__main__":
    # 设置参数
    n_values = [5, 7, 10, 20, 30, 50, 100, 200, 500, 1000]
    num_simulations = 10000  # 每个n的模拟次数
    top_percent = 0.1  # 前10%

    # 运行模拟
    print("开始模拟37%法则...")
    results = run_simulations(n_values, num_simulations, top_percent)

    # 打印详细结果
    print_detailed_results(results)

    # 可视化结果
    print("\n生成可视化图表...")
    plot_results(results)

    # 额外: 对特定n值进行更详细的模拟
    print("\n" + "=" * 80)
    print("对n=30的详细分析")
    print("=" * 80)

    n_detail = 30
    result_detail = simulate_optimal_stopping(n_detail, 100000, top_percent=0.1)

    print(f"追求者数量: {n_detail}")
    print(f"最优k值: {result_detail['k']}")
    print(f"模拟次数: {result_detail['num_simulations']:,}")
    print(f"选中最佳追求者的概率: {result_detail['best_prob']:.4f} ({result_detail['best_prob'] * 100:.2f}%)")
    print(f"前10%阈值质量值: >= {result_detail['threshold']}")
    print(
        f"选中前10%追求者的概率: {result_detail['top_percent_prob']:.4f} ({result_detail['top_percent_prob'] * 100:.2f}%)")

    # 计算质量分布
    rank_counts = result_detail['rank_counts']
    top_ranks = sorted(rank_counts.keys(), reverse=True)[:10]  # 前10个最常被选中的质量排名

    print(f"\n最常被选中的前10个质量排名:")
    for rank in top_ranks:
        count = rank_counts[rank]
        prob = count / result_detail['num_simulations']
        print(f"  质量排名 {rank}: {count}次 ({prob * 100:.2f}%)")