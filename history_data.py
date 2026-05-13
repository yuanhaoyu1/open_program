from datetime import datetime, timedelta
from pathlib import Path
import random
from typing import List
class history_data:
    def __init__(self):
        self.data_dir = Path("./history_data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    def _get_file_path(self, date_str: str) -> Path:
        """获取对应日期的文件路径"""
        date_obj = datetime.strptime(date_str, "%Y-%m-%d-%H")
        date_dir = self.data_dir / date_obj.strftime("%Y-%m-%d")
        return date_dir / f"{date_obj.strftime('%Y-%m-%d')}.txt"
    def get_data(self, date: str) -> str:
        """获取指定时间的历史数据"""
        try:
            file_path = self._get_file_path(date)
            target_hour = datetime.strptime(date, "%Y-%m-%d-%H").hour

            with file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line_time = datetime.fromisoformat(line.split("   ")[0])
                    if line_time.hour == target_hour:
                        return line
        except (FileNotFoundError, IsADirectoryError):
            pass
        # 生成模拟数据
        return self._generate_simulated_data(date)
    def _generate_simulated_data(self, date_str: str) -> str:
        """生成模拟数据"""
        date_obj = datetime.strptime(date_str, "%Y-%m-%d-%H")
        base_time = datetime.combine(date_obj.date(), datetime.now().time())
        return (
            f"{base_time.isoformat()}   "
            f"{random.randint(10, 20)}   "
            f"{random.randint(10, 20)}   "
            f"{random.randint(1, 10)}\n"
        )
    def store_data(self, temp: float, humi: float, co2: float):
        """存储传感器数据"""
        timestamp = datetime.now()
        file_path = self._get_file_path(timestamp.strftime("%Y-%m-%d-%H"))
        # 确保目录存在
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(f"{timestamp.isoformat()}   {temp}   {humi}   {co2}\n")
def one_day(current_time_str: str) -> List[str]:
    """生成24小时时间列表"""
    current_time = datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S")
    return [
        (current_time - timedelta(hours=hours)).strftime("%Y-%m-%d-%H")
        for hours in range(24, -1, -1)
    ]
def chaxun(current_time_str: str) -> List[List[str]]:
    """查询24小时历史数据"""
    hd = history_data()
    return [
        [date] + hd.get_data(date).strip().split("   ")[1:]
        for date in one_day(current_time_str)
    ]
def format_time(time_str: str) -> str:
    """格式化时间字符串"""
    date_part = datetime.strptime(time_str, "%Y-%m-%d-%H")
    return datetime.combine(date_part.date(), datetime.now().time()).isoformat()
if __name__ == "__main__":
    sample_data = chaxun("2024-03-18 17:09:00")
    for item in sample_data:
        print(item)