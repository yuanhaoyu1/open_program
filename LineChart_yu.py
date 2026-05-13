# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtGui import QPainter, QFont, QColor

minTime=0
maxTime=24
class LineChart(QMainWindow):
    def __init__(self,chaet_name):
        super().__init__()
        self.chart_name = chaet_name
        self.weather_datas = []
        series = QLineSeries()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setStyleSheet('''
                    QMainWindow {  
                                       background-color:transparent; /* 黑蓝色背景 */  
                                       color: white; /* 文本颜色为白色，以便在黑蓝色背景上可见 */  
                                   }  
        ''')
        txt_address = "./weather/temperature_data.txt"
        with open(txt_address, 'r') as file:
            for line in file:
                time, weather_data = map(int, line.strip().split())
                self.weather_datas.append(weather_data)
                series.append(time, weather_data)

        chart = QChart()
        chart.setTitleFont(QFont("Arial", 10, QFont.Bold))
        chart.setTitleBrush(QColor(255, 255, 255, 100))
        chart.setBackgroundVisible(False)  # 设置背景透明
        chart.setTheme(QChart.ChartThemeBlueCerulean)
        chart.addSeries(series)
        axisX = QValueAxis()
        axisY = QValueAxis()
        axisX.setReverse(False)
        axisX.setRange(minTime, maxTime)  # 设置 X 轴的范围
        axisX.setTickCount(9)

        axisX.setLabelFormat("%.0f")  # 设置 X 轴标签格式为整数
        axisY.setRange(min(self.weather_datas)-4, max(self.weather_datas)+4)  # 设置 Y 轴的范围
        axisY.setTickCount(6)

        axisY.setTitleText(f"{self.chart_name}")  # 设置 Y 轴的标题
        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignRight)


        legend = chart.legend()
        legend.setVisible(False)


        chart.setTitle(f"农田24小时内的{self.chart_name}")    #折线图标题

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        # chartView.setChart(chart)
        chartView.resize(500,270)


        #
        self.setCentralWidget(chartView)
        self.setGeometry(100, 100, 1500, 1000)   #界面坐标及大小
        self.setWindowTitle('PyQt Line Chart')   #界面标题
        chartView.setStyleSheet("""
            QChartView {
                background-color: transparent; /* 背景颜色及透明度 */
                color:white;
                border:none;
                margin: none;
            }
            QChart::frame {
                border: none; /* 去除阴影边框 */
    }
        """)


        # 将图表视图添加到透明的QWidget中
        layout = QVBoxLayout(self)
        layout.addWidget(chartView)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.dragPos:
            return
        if event.buttons() & Qt.LeftButton:
            # 更新窗口的位置
            self.move(event.globalPos() - self.dragPos)
            event.accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window1,window2,window3 = LineChart("温度"),LineChart("光照"),LineChart("CO2浓度")
    window1.show(),window2.show(),window3.show()
    sys.exit(app.exec_())