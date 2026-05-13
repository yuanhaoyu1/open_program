# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPainter
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QCategoryAxis, QValueAxis
from history_data import chaxun


class LineChart(QMainWindow):
    def __init__(self, chart_name, data_type_index):
        super().__init__()
        self.chart_name = chart_name
        self.data_type_index = data_type_index
        self.setup_ui()
        self.load_data()
        self.setFixedSize(600, 300)

    def setup_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setStyleSheet('''
            QMainWindow { background-color: transparent; color: white; }
        ''')

    def load_data(self):
        # 获取当前时间并生成完整时间序列
        now = datetime.now()
        current_hour = now.hour
        raw_data = chaxun(now.strftime("%Y-%m-%d %H:%M:%S"))

        # 初始化两条折线（今天和昨天）
        today_series = QLineSeries()
        yesterday_series = QLineSeries()
        today_series.setName("今天")
        yesterday_series.setName("昨天")
        today_series.setColor(QColor(0, 255, 0))  # 绿色
        yesterday_series.setColor(QColor(0, 0, 255))  # 蓝色

        # 填充数据点
        for item in raw_data:
            try:
                dt = datetime.strptime(item[0], "%Y-%m-%d-%H")
                value = float(item[self.data_type_index])

                # 计算与当前时间的小时差并转换为X轴位置
                time_diff = now - dt
                hours_ago = int(time_diff.total_seconds() // 3600)
                x = 24 - hours_ago  # X=0表示24小时前，X=24表示当前时间

                if 0 <= x <= 24:
                    if dt.date() == now.date():
                        today_series.append(x, value)
                    else:
                        yesterday_series.append(x, value)
            except Exception as e:
                print(f"数据错误: {e}")

        # 创建图表
        chart = QChart()
        chart.addSeries(today_series)
        chart.addSeries(yesterday_series)
        chart.setTitle(f"近24小时{self.chart_name}变化")
        chart.legend().setVisible(True)

        # 配置横坐标（时间轴）
        axisX = QCategoryAxis()
        axisX.setRange(0, 24)
        axisX.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)

        # 动态生成小时标签（稀疏显示）
        label_interval = 3  # 每3小时显示一个标签
        for x in range(0, 25, label_interval):
            hour_label = int((current_hour - 24 + x) % 24)
            axisX.append(f"{hour_label:02d}时", x)

        # 配置纵坐标
        axisY = QValueAxis()
        all_values = [p.y() for s in [today_series, yesterday_series] for p in s.pointsVector()]
        y_min = min(all_values) if all_values else 0
        y_max = max(all_values) if all_values else 100
        axisY.setRange(y_min * 0.9, y_max * 1.1)
        axisY.setTitleText(self.chart_name)

        # 添加坐标轴
        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        today_series.attachAxis(axisX)
        today_series.attachAxis(axisY)
        yesterday_series.attachAxis(axisX)
        yesterday_series.attachAxis(axisY)

        # 样式设置
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        chartView.setStyleSheet("""
            QChartView { background: transparent; }
            QChart::title { color: white; font-size: 14px; }
            QLegend { color: white; }
        """)
        self.setCentralWidget(chartView)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    charts = [
        LineChart("温度", 1),
        LineChart("湿度", 2),
        LineChart("CO₂浓度", 3)
    ]
    for chart in charts:
        chart.show()
    sys.exit(app.exec_())