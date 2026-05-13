import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,QHeaderView, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
from weather import weather_get
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QMouseEvent
class WeatherInfoWindow(QMainWindow):
    def __init__(self,mode="dark"):
        super().__init__()
        self.mode=mode
        self.initUI()
    def initUI(self):
        self.setWindowTitle('详细天气信息')
        self.setGeometry(350, 300, 1200,500)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)


        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        if self.mode == 'dark':
            self.central_widget.setStyleSheet("""
                                                  QWidget {
                                                      background-color: rgba(17, 31, 51, 200); /* 背景颜色及透明度 */
                                                      border-radius: 10px; /* 设置圆角 */
                                                  }
                                              """)

        else:
            self.central_widget.setStyleSheet("""
                                                  QWidget {
                                                      background-color: rgba(255, 255,255, 200); /* 背景颜色及透明度 */
                                                      border-radius: 10px; /* 设置圆角 */
                                                  }
                                              """)

        # 创建一个表格用于显示天气信息
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)  # 假设有5行数据
        self.tableWidget.setColumnCount(9)  # 假设有3列数据
        self.tableWidget.setHorizontalHeaderLabels(['日期', '白天天气','夜间天气','白天温度','夜间温度','白天风向','夜间风向','白天风级','夜间风级'])

        # 设置表格的水平和垂直表头样式
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏垂直表头

        # 设置表格字体和大小
        font = QFont("Arial", 10)
        self.tableWidget.setFont(font)


        # 应用样式表美化表格
        if self.mode=="dark":
            self.tableWidget.setStyleSheet("""  
                QTableWidget {    
                    background-color: rgba(17, 31, 51, 200);    
                    border: 1px solid #d0d0d0;    
                    border-radius: 5px;    
                    font: 12pt "Arial"; /* 设置表格字体大小和字体类型 */  
                    color: white /* 设置表格文本颜色 */  
                }  
                QTableWidget::item {    
                    border-bottom: 1px solid #d0d0d0;    
                    padding: 5px;    
                }  
                QTableWidget::item:selected {    
                    background-color: #a0a0a0;    
                    color: white; /* 选中项的文本颜色 */  
                }  
                QTableWidget QHeaderView::section {  /* 专门针对QTableWidget的表头设置样式 */  
                    background-color: #111F33; /* 设置表头背景色为蓝黑色 */  
                    color: white; /* 设置表头字体颜色为白色 */  
                    border: 1px solid #d0d0d0; /* 设置表头边框 */  
                    padding: 4px; /* 设置表头内边距 */  
                    text-align: center; /* 设置表头文本居中 */  
                }  
            """)
        else:
            self.tableWidget.setStyleSheet("""  
                       QTableWidget {  
                           background-color:  rgba(255, 255,255, 200);  
                           border: 1px solid #d0d0d0;  
                           border-radius: 5px;  
                       }  
                       QTableWidget::item {  
                           border-bottom: 1px solid #d0d0d0;  
                           padding: 5px;  
                       }  
                       QTableWidget::item:selected {  
                           background-color: #a0a0a0;  
                       }  
                   """)

        # 填充一些示例数据

        self.weather_info=weather_get().get_weather_detail()
        print(self.weather_info)
        for i in range(4):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(self.weather_info[i]['date']))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(self.weather_info[i]['dayweather']))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(self.weather_info[i]['nightweather']))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(self.weather_info[i]['daytemp']))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(self.weather_info[i]['nighttemp']))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(self.weather_info[i]['daywind']))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(self.weather_info[i]['nightwind']))
            self.tableWidget.setItem(i, 7, QTableWidgetItem(self.weather_info[i]['daypower']))
            self.tableWidget.setItem(i, 8, QTableWidgetItem(self.weather_info[i]['nightpower']))



        self.little_layout=QHBoxLayout()
        close_button = QPushButton(self)  # 创建关闭按钮
        close_button.setGeometry(10, 10, 80, 30)  # 设置按钮位置和大小
        close_button.setText('关闭')  # 设置按钮文本
        close_button.setFixedSize(80, 30)  # 设置宽度为80像素，高度为30像素

        close_button.clicked.connect(self.close)  # 关联按钮点击事件和关闭窗口的方法

        minimize_button = QPushButton(self)
        minimize_button.setGeometry(100, 10, 80, 30)  # 设置按钮位置和大小
        minimize_button.setText('最小化')  # 设置按钮文本
        minimize_button.setFixedSize(80, 30)  # 设置宽度为80像素，高度为30像素

        minimize_button.clicked.connect(self.showMinimized)  # 关联按钮点击事件与窗口最小化方法

        # 创建全屏切换按钮
        fullscreen_button = QPushButton(self)
        fullscreen_button.setGeometry(190, 10, 80, 30)  # 设置按钮位置和大小
        fullscreen_button.setText('窗口化')  # 设置按钮文本
        fullscreen_button.setFixedSize(80, 30)  # 设置宽度为80像素，高度为30像素

        fullscreen_button.clicked.connect(self.toggleFullScreen)  # 关联按钮点击事件与全屏切换方法
        self.little_layout.addWidget(close_button)
        self.little_layout.addWidget(minimize_button)
        self.little_layout.addWidget(fullscreen_button)
        self.spacer = QSpacerItem(900, 30, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.little_layout.addItem(self.spacer)


        layout.addLayout(self.little_layout)
        layout.addWidget(self.tableWidget)


        close_button.setStyleSheet("""
                        QPushButton {
                            border-radius: 15px; /* 半径为宽度的一半 */
                            border: none;
                            color: white;
                            background-color: grey;
                        }
                        QPushButton:hover {
                            background-color: darkred;
                        }
                        QPushButton:pressed {
                            background-color: lightcoral;
                        }
                    """)

        fullscreen_button.setStyleSheet("""
                    QPushButton {
                        border-radius: 15px; /* 半径为宽度的一半 */
                        border: none;
                        color: white;
                        background-color: grey;
                    }
                    QPushButton:hover {
                        background-color: darkred;
                    }
                    QPushButton:pressed {
                        background-color: lightcoral;
                    }
                """)
        minimize_button.setStyleSheet("""
                            QPushButton {
                                border-radius: 15px; /* 半径为宽度的一半 */
                                border: none;
                                color: white;
                                background-color: grey;
                            }
                            QPushButton:hover {
                                background-color: darkred;
                            }
                            QPushButton:pressed {
                                background-color: lightcoral;
                            }
                        """)

    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

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


if __name__=="__main__":
    app=QApplication(sys.argv)
    info_window=WeatherInfoWindow(mode="bright")
    info_window.show()
    sys.exit(app.exec_())
