import random
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QHeaderView, QMessageBox, \
    QFileDialog, QApplication, QLabel, QTableView
from PyQt5.QtGui import QImage, QPixmap, QStandardItemModel, QStandardItem, QMouseEvent
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime, timedelta
import sys
from weather import weather_get
from CO2_light import ChinaEnvironmentMonitor
from detail_weather_info import WeatherInfoWindow
from history_data import chaxun,history_data
from LineChart import LineChart
#对UI界面的两种模式进行设置：dark模式与bright模式
dark_StyleSheet="""  
                       QMainWindow {  
                           background-color: #111F33; /* 黑蓝色背景 */  
                           color: white; /* 文本颜色为白色，以便在黑蓝色背景上可见 */  
                       }  
                        QLabel {  
                                border: 2px solid #888; /* 设置边框宽度、样式和颜色 */  
                                padding: 5px; /* 设置内边距 */  
                                font-size: 14pt; /* 设置字体大小 */  
                                color: white; /* 设置字体颜色为白色 */
                            }  
                       /* 你可以在这里添加更多部件的样式定义 */  
                   """
bright_StyleSheet="""  
                       QMainWindow {  
                           background-color: #F0F0F0; /* 白色背景 */  
                           color: black; /* 文本颜色为黑色，以便在白色背景上可见 */  
                       }  
                       QLabel {  
                                border: 2px solid #888; /* 设置边框宽度、样式和颜色 */  
                                padding: 5px; /* 设置内边距 */  
                                font-size: 14pt; /* 设置字体大小 */  
                                color: black; /* 设置字体颜色为黑色 */
                            }  
                       /* 你可以在这里添加更多部件的样式定义 */  
                   """
class VideoWindow(QMainWindow):
    #对最开始的主窗口进行初始化
    def __init__(self):
        super().__init__()
        self.mode = "dark"
        self.is_camera_mode = True
        self.current_video_path = None
        self.cap = None  # 初始化视频捕获对象为None
        # 初始化历史数据存储
        self.hd = history_data()  # 创建 history_data 实例
        # 生成并保存当天和前一天的模拟数据
        self.generate_and_save_historical_data()
        self.initUI()
        self.init_video_capture()  # 统一初始化视频源
    def generate_and_save_historical_data(self):
        """生成并保存当天和前一天的模拟数据"""
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        # 生成并保存当天的数据
        for hour in range(24):  # 生成24小时的数据
            date_str = now.strftime("%Y-%m-%d") + f"-{hour:02d}"
            self.hd.store_data(
                temp=random.randint(10, 20),
                humi=random.randint(10, 20),
                co2=random.randint(1, 10)
            )
        # 生成并保存前一天的数据
        for hour in range(24):  # 生成24小时的数据
            date_str = yesterday.strftime("%Y-%m-%d") + f"-{hour:02d}"
            self.hd.store_data(
                temp=random.randint(10, 20),
                humi=random.randint(10, 20),
                co2=random.randint(1, 10)
            )
    def initUI(self):
        self.setWindowTitle('基于类脑智能的农业环境检测系统')  # 窗口名称
        self.setGeometry(100, 50, 1600, 1000)  # 设置窗口的初始位置与长宽
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        mainmain_layout = QHBoxLayout()
        mainmainmain_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(mainmainmain_layout)
        self.setCentralWidget(self.central_widget)
        # --- 创建标题标签 ---
        self.title_label = QLabel("基于类脑智能的农业环境检测系统")
        self.title_label.setStyleSheet('''  
               QLabel {  
                   background-color: transparent;  
                   border: none;    
                   padding: 5px;    
                   font-family: "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;  
                   font-weight: bold;  
                   font-size: 20pt;  
                   color: white;  
               }    
           ''')
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        #对三个表格进行设置
        chart1 = LineChart("温度", 1)  # 1对应温度数据索引
        chart2 = LineChart("光照", 2)  # 4对应光照数据索引（根据实际数据位置调整）
        chart3 = LineChart("CO2浓度", 3)  # 3对应CO2数据索引
        chart1.setStyleSheet(
            '''
                LineChart {
                    border: 1px solid black;   /* 给图表添加边框 */
                    background-color: transparent;  /* 设置背景颜色 */
                }

                LineChart QWidget {    /* 如果LineChart内部有特定的QWidget需要设置样式，可以在这里定义 */
                    font-size: 12px;
                    color: #333;
                    background-color:transparent;
                }
            '''
        )
        chart2.setStyleSheet(
            '''
                LineChart {
                    border: 1px solid black;   /* 给图表添加边框 */
                    background-color: transparent;  /* 设置背景颜色 */
                }

                LineChart QWidget {    /* 如果LineChart内部有特定的QWidget需要设置样式，可以在这里定义 */
                    font-size: 12px;
                    color: #333;
                    background-color:transparent;
                }
            '''
        )
        chart3.setStyleSheet(
            '''
                LineChart {
                    border: 1px solid black;   /* 给图表添加边框 */
                    background-color: transparent;  /* 设置背景颜色 */
                }

                LineChart QWidget {    /* 如果LineChart内部有特定的QWidget需要设置样式，可以在这里定义 */
                    font-size: 12px;
                    color: #333;
                    background-color:transparent;
                }
            '''
        )
        # 创建主布局
        main_layout = QVBoxLayout()
        vice_layout=QVBoxLayout()
        linechart=QHBoxLayout()
        linechart.addWidget(chart1)
        linechart.addWidget(chart2)
        linechart.addWidget(chart3)
        mainmain_layout.addLayout(main_layout)
        mainmain_layout.addLayout(vice_layout)
        mainmainmain_layout.addLayout(mainmain_layout)
        mainmainmain_layout.addLayout(linechart)
        little_layout=QVBoxLayout()
        vice_layout.addLayout(little_layout)
        self.weather_label=[]
        self.area_label = QLabel("所在地区：郑州")  # 初始化时设置默认值
        self.area_label.setAlignment(Qt.AlignCenter)
        self.area_label.setStyleSheet("""
            QLabel {
                font-size: 16pt;
                padding: 8px;
                border-bottom: 2px solid #888;
            }
        """)
        little_layout.addWidget(self.area_label)
        # 获取城市并更新显示
        try:
            chaxun = weather_get()
            city = chaxun.get_city_by_ip()
            self.area_label.setText(f"所在地区：{city}")
        except Exception as e:
            print(f"获取城市失败: {str(e)}")
        weather_data = [
            {"date": "今  天", "weather": "Cloudy", "temp": "22°C"},
            {"date": "明  天 ", "weather": "Rainy", "temp": "20°C"},
            {"date": "后  天", "weather": "Sunny", "temp": "25°C"},
        ]
        # 遍历天气数据并创建标签
        for data in weather_data:
            # 创建天气信息的标签
            weather_label = QLabel(f"{data['date']}: {data['weather']}, {data['temp']}°C")
            self.weather_label.append(weather_label)
            little_layout.addWidget(weather_label)
        self.updateweather()
        self.weather_timer = QTimer(self)
        self.weather_timer.timeout.connect(self.updateweather)
        self.weather_timer.start(600000)
        self.button_detail = QPushButton("详细天气信息")
        little_layout.addWidget(self.button_detail)
        self.button_detail.clicked.connect(self.show_detail)
        self.update_theme(self.mode)
        self.model = QStandardItemModel(25, 4, self)  # 0行，2列
        self.model.setHorizontalHeaderLabels(['Time', 'Temper','Co2','Humidty'])
        # 创建视图
        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setFixedHeight(500)  # 设置表格视图的高度为200像素
        self.tableView.setStyleSheet("""  
                   QTableView {  
                       background-color: rgba(255, 255, 255, 180);  
                       border: 1px solid #d3d3d3;  
                       selection-background-color: rgba(255, 127, 127, 120);  
                   }  
                   QScrollBar:vertical {  
                       border: none;  
                       background: rgba(255, 255, 255, 0);  
                       width: 15px;  
                       margin: 0px 0px 0px 0px;  
                   }  
                   QScrollBar:horizontal {  
                       border: none;  
                       background: rgba(255, 255, 255, 180);  
                       height: 15px;  
                       margin: 0px 0px 0px 0px;  
                   }  
                   QScrollBar::handle:vertical {  
                       background: rgba(128, 128, 128, 180);  
                       min-height: 20px;  
                   }  
                   QScrollBar::handle:horizontal {  
                       background: rgba(128, 128, 128, 180);  
                       min-width: 20px;  
                   }  
                   QScrollBar::add-line:vertical {  
                       border: none;  
                       background: none;  
                       height: 0;  
                       subcontrol-position: bottom;  
                       subcontrol-origin: margin;  
                   }  
                   QScrollBar::sub-line:vertical {  
                       border: none;  
                       background: none;  
                       height: 0;  
                       subcontrol-position: top;  
                       subcontrol-origin: margin;  
                   }  
                   QScrollBar::add-line:horizontal {  
                       border: none;  
                       background: none;  
                       width: 0;  
                       subcontrol-position: right;  
                       subcontrol-origin: margin;  
                   }  
                   QScrollBar::sub-line:horizontal {  
                       border: none;  
                       background: none;  
                       width: 0;  
                       subcontrol-position: left;  
                       subcontrol-origin: margin;  
                   }  
                   QHeaderView::section {  
                        border: none;  
                        background-color: rgba(255, 255, 255, 180);   
                        padding: 2px;  
                    }  
                QHeaderView::section:horizontal {  
                    min-height: 15px;  
                }  
                QHeaderView::section:vertical {  
                    min-width: 17px;  
                    border-radius: 0px;
                }  
                               """)
        # 添加视图到布局
        little_layout.addWidget(self.tableView)
        # 设置定时器来更新表格数据
        self.updateTable()
        self.table_timer = QTimer(self)
        self.table_timer.timeout.connect(self.updateTable)
        self.table_timer.start(3600000)
        self.title_label.setStyleSheet('''  
            QLabel {  
                background-color: transparent; /* 新增：将背景色设置为透明 */  
                border: none; /* 设置边框样式为无 */    
                padding: 5px; /* 设置内边距 */    
                font-family: "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif; /* 设置字体家族，使用常用中文黑体 */  
                font-weight: bold; /* 字体加粗 */  
                font-size: 20pt; /* 字体大小设置为20磅，比原来的14磅更大 */  
                color: white; /* 字体颜色为白色 */  
            }    
        ''')
        main_layout.addWidget(self.title_label)
        self.label = QLabel(self)
        self.label.setFixedSize(600,400)
        main_layout.addWidget(self.label)
        # 创建数据展示框和按键
        data_layout = QHBoxLayout()
        main_layout.addLayout(data_layout)
        # 数据展示框
        self.data_labels = [
            QLabel('密度:', self),
            QLabel('温度:', self),
            QLabel('湿度:', self),
            QLabel('CO₂:', self),  # 明确标签
            QLabel('光照:', self)
        ]
        for label in self.data_labels:
            data_layout.addWidget(label)
            label.setFixedSize(160,40)
        self.label_timer = QTimer(self)
        self.label_timer.timeout.connect(self.updateLabel)
        self.label_timer.start(5000)
        button_layout = QHBoxLayout()
            # 按键
        self.buttons = [QPushButton("视频模式"), QPushButton("预 警"), QPushButton("模 式")]
        for button in self.buttons:
            button.setStyleSheet("""  
                            QPushButton {  
                                background-color: #ddd; /* 背景颜色 */  
                                border: 2px solid #888; /* 边框 */  
                                border-radius: 5px; /* 边框圆角 */  
                                color: #333; /* 字体颜色 */  
                                padding: 10px 20px; /* 内边距 */  
                                font-size: 12pt; /* 字体大小 */  
                            }  

                            QPushButton:hover {  
                                background-color: #ccc; /* 鼠标悬停时的背景颜色 */  
                            }  

                            QPushButton:pressed {  
                                background-color: #bbb; /* 按下时的背景颜色 */  
                            }  
                        """)

            button_layout.addWidget(button)
            button.setFixedSize(130, 50)
        self.buttons[0].clicked.connect(self.on_button_clicked1)
        self.buttons[1].clicked.connect(self.on_button_clicked2)
        self.buttons[2].clicked.connect(self.on_button_clicked3)
        main_layout.addLayout(button_layout)
        data_layout.setSpacing(30)
        data_layout.setAlignment(Qt.AlignLeft)
        button_layout.setSpacing(180)
        button_layout.setContentsMargins(10, 10, 10, 10)
        button_layout.setAlignment(Qt.AlignLeft)
        # 设置中央控件和布局
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(30)  # update every 30 ms
        self.net = cv2.dnn.readNet("custom-yolov4-tiny-detector_best.weights", "custom-yolov4-tiny-detector.cfg")
        self.classes = ["tomato"]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        close_button = QPushButton(self)  # 创建关闭按钮
        close_button.setGeometry(10, 10, 80, 30)  # 设置按钮位置和大小
        close_button.setText('关闭')  # 设置按钮文本
        close_button.clicked.connect(self.close)  # 关联按钮点击事件和关闭窗口的方法
        minimize_button = QPushButton(self)
        minimize_button.setGeometry(100, 10, 80, 30)  # 设置按钮位置和大小
        minimize_button.setText('最小化')  # 设置按钮文本
        minimize_button.clicked.connect(self.showMinimized)  # 关联按钮点击事件与窗口最小化方法
        # 创建全屏切换按钮
        fullscreen_button = QPushButton(self)
        fullscreen_button.setGeometry(190, 10, 80, 30)  # 设置按钮位置和大小
        fullscreen_button.setText('窗口化')  # 设置按钮文本
        fullscreen_button.clicked.connect(self.toggleFullScreen)  # 关联按钮点击事件与全屏切换方法
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
        self.update_theme(self.mode)
    def init_video_capture(self):
        """统一初始化视频源"""
        if self.is_camera_mode:
            self.init_camera()
        else:
            self.init_video_file()
        if self.cap and self.cap.isOpened():
            # 初始化定时器
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateFrame)
            self.timer.start(30)
            # 初始化神经网络
            self.net = cv2.dnn.readNet("custom-yolov4-tiny-detector_best.weights",
                                       "custom-yolov4-tiny-detector.cfg")
            self.classes = ["tomato"]
            self.layer_names = self.net.getLayerNames()
            self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
            self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
    def init_camera(self):
        """初始化摄像头"""
        if self.cap:
            self.cap.release()
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Windows专用
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)  # 回退到默认方式
        except:
            self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            QMessageBox.critical(self, "错误", "无法打开摄像头")
            return False
        # 设置摄像头参数
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return True
    def init_video_file(self, path=None):
        """初始化视频文件"""
        if not path:
            path, _ = QFileDialog.getOpenFileName(
                self,
                "选择视频文件",
                "",
                "Video Files (*.mp4 *.avi *.mov)"
            )
            if not path:
                return False
        if hasattr(self, 'cap'):
            self.cap.release()
        self.current_video_path = path
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            QMessageBox.critical(self, "错误", "无法打开视频文件")
            return False
        return True
    def on_button_clicked1(self):
        """切换摄像头/视频模式"""
        try:
            # 切换模式
            self.is_camera_mode = not self.is_camera_mode

            if self.is_camera_mode:
                # 切换到摄像头模式ad
                if self.init_camera():
                    self.buttons[0].setText("摄像头模式")
            else:
                # 切换到视频文件模式
                if self.init_video_file():
                    self.buttons[0].setText("视频模式")
                else:
                    # 如果用户取消选择，恢复模式状态
                    self.is_camera_mode = not self.is_camera_mode
            # 重置显示尺寸
            if self.cap.isOpened():
                width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.label.setFixedSize(width // 2, height // 2)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"模式切换失败: {str(e)}")
    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    def updateweather(self):
        chaxun=weather_get()
        self.live_weather,self.for_weather,self.live_temp,self.for_temp,self.for_weather_two,self.for_temp_two=chaxun.get_weather()
        weather_data = [
            {"date": "今  天", "weather": self.live_weather, "temp": self.live_temp},
            {"date": "明  天 ", "weather": self.for_weather, "temp": self.for_temp},
            {"date": "后  天", "weather": self.for_weather_two, "temp": self.for_temp_two},
        ]
        for i, data in enumerate(weather_data):
            # 获取对应的标签（假设它们已经被存储在self.weather_labels列表中）
            weather_label = self.weather_label[i]
            # 更新标签的文本
            weather_label.setText(f"{data['date']}: {data['weather']}, {data['temp']}")
    def updateTable(self):
        current_time = datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.data_list=[]
        self.data_list=chaxun(current_time_str)
        # print(self.data_list)
        for row_index, row_data in enumerate(self.data_list):
            for col_index, value in enumerate(row_data[0:4], start=1):  # 从第二个元素开始，取三个元素
                item = QStandardItem(value.strip())  # 去除换行符并创建标准项
                self.model.setItem(row_index, col_index - 1, item)  # 设置模型项（注意列索引从0开始）
        pass
    def updateFrame(self):
        if self.cap and self.cap.isOpened():
            # 视频循环检测
            if not self.is_camera_mode:
                if self.cap.get(cv2.CAP_PROP_POS_FRAMES) >= self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, img = self.cap.read()
            if not success:
                self.label.setText("视频源读取失败")
                return
            # 保持目标检测代码完整
            img = cv2.resize(img, None, fx=0.5, fy=0.5)
            height, width, channels = img.shape
            # YOLO目标检测
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.15:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            font = cv2.FONT_HERSHEY_PLAIN
            self.midu = len(boxes)/10
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    color = self.colors[class_ids[i]]
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, label, (x, y + 30), font, 1, color, 2)
            # 修正颜色转换
            rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 修正参数
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
            self.label.setPixmap(QPixmap.fromImage(p))
    def closeEvent(self, event):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        super().closeEvent(event)
    def show_detail(self):
        self.info_window = WeatherInfoWindow(self.mode)
        self.info_window.show()
    def updateLabel(self):
        try:
            # 初始化环境监测器
            env_monitor = ChinaEnvironmentMonitor()
            # 获取环境数据
            co2_level = env_monitor.get_co2_simulation()
            light_intensity = env_monitor.get_light_intensity()
            # 从天气接口获取实时数据
            weather = weather_get()
            live_weather, _, temp, humidity, *_ = weather.get_weather()
            # 更新数据标签
            self.data_labels[0].setText(f'密度: {self.midu:.1f}')
            self.data_labels[1].setText(f'温度: {temp}℃')  # 使用API温度数据
            self.data_labels[2].setText(f'湿度: {humidity}%')  # 使用API湿度数据
            self.data_labels[3].setText(f'CO₂: {co2_level}ppm')  # 新增CO₂显示
            self.data_labels[4].setText(f'光照: {light_intensity}lux')  # 新增光照显示
        except Exception as e:
            print(f"数据获取失败: {str(e)}")
            # 失败时显示默认信息
            self.data_labels[1].setText('温度: --')
            self.data_labels[2].setText('湿度: --')
            self.data_labels[3].setText('CO₂: --')
            self.data_labels[4].setText('光照: --')
    def calculate_data(self):
        return 123, 456, 789
    def on_button_clicked1(self):  # 保留一个正确定义
        """切换摄像头/视频模式"""
        try:
            self.is_camera_mode = not self.is_camera_mode
            if self.is_camera_mode:
                if self.init_camera():
                    self.buttons[0].setText("视频模式")
                    self.timer.start(30)
            else:
                if self.init_video_file():
                    self.buttons[0].setText("摄像头模式")
                    self.timer.start(30)
                else:
                    self.is_camera_mode = not self.is_camera_mode
            if self.cap.isOpened():
                width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.label.setFixedSize(width//2, height//2)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"模式切换失败: {str(e)}")
    def on_button_clicked2(self):
       # 添加按键的处理逻辑
        pass
    def on_button_clicked3(self):
        if self.mode=="dark":
            self.mode="bright"
        else:
            self.mode="dark"
        self.update_theme(self.mode)
    def update_theme(self, theme):
        # 根据当前主题更新样式表
        if self.mode == 'dark':
            self.setStyleSheet(dark_StyleSheet)
            # 设置标题字体颜色为白色
            self.title_label.setStyleSheet('''
                QLabel {  
                    background-color: transparent;  
                    border: none;    
                    padding: 5px;    
                    font-family: "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;  
                    font-weight: bold;  
                    font-size: 20pt;  
                    color: white;  
                }    
            ''')
        elif self.mode == 'bright':
            self.setStyleSheet(bright_StyleSheet)
            # 设置标题字体颜色为黑色
            self.title_label.setStyleSheet('''
                QLabel {  
                    background-color: transparent;  
                    border: none;    
                    padding: 5px;    
                    font-family: "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;  
                    font-weight: bold;  
                    font-size: 20pt;  
                    color: black;  
                }    
            ''')
        # 更新中央控件的样式
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
                    background-color: rgba(255, 255, 255, 200); /* 背景颜色及透明度 */
                    border-radius: 10px; /* 设置圆角 */
                }
            """)
        # 更新按钮样式
        if self.mode == "dark":
            self.button_detail.setStyleSheet("""  
                QPushButton {  
                    border: 1px solid #ccc;  
                    border-radius: 5px;  
                    color: white; /* 字体颜色 */  
                    padding: 5px 10px;  
                    margin-right: 10px; /* 右侧外边距 */  
                    font-size: 10pt;  
                }  
            """)
        else:
            self.button_detail.setStyleSheet("""  
                QPushButton {  
                    border: 1px solid #ccc;  
                    border-radius: 5px;  
                    color: black; /* 字体颜色 */  
                    padding: 5px 10px;  
                    margin-right: 10px; /* 右侧外边距 */  
                    font-size: 10pt;  
                }  
            """)
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
    def closeEvent(self, event):  # 保留一个正确定义
        if self.cap and self.cap.isOpened():
            self.cap.release()
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        super().closeEvent(event)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoWindow()
    ex.show()
    sys.exit(app.exec_())