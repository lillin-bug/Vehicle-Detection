#coding:utf-8
import sys,os
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtCore import QTimer
import Trafficstatistics

path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class MainWindow(QtWidgets.QMainWindow) :

    def __init__(self):
        super().__init__()
        self.initUI()



    def initUI(self):
        self.setWindowTitle("基于计算机视觉的交通场景")
        self.setGeometry(300,180,1480,700)
        self.main_widget = QtWidgets.QWidget() #创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout) #设置窗口主部件为网格布局
        self.main_widget.setStyleSheet("background-color:rgb(126,126,135)")

        self.left_widget = QtWidgets.QWidget() #创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout) #设置左侧部件为网格布局

        self.video_widget = QtWidgets.QWidget() #创建video位置部件
        self.video_widget.setObjectName('video_widget')
        self.video_layout = QtWidgets.QGridLayout()
        self.video_widget.setLayout(self.video_layout)  #设置video位置为网格布局

        self.output_widget = QtWidgets.QWidget()  # 创建输出位置部件
        self.output_widget.setObjectName('output_widget')
        self.output_layout = QtWidgets.QGridLayout()
        self.output_widget.setLayout(self.output_layout)  # 设置输出位置为网格布局
        self.output_widget.setStyleSheet("color:white")
        self.output_widget.setStyleSheet("color:white") #使用说明字体颜色

        self.main_layout.addWidget(self.left_widget, 0, 0, 8, 2)
        self.main_layout.addWidget(self.video_widget, 0, 3, 8, 12)
        self.main_layout.addWidget(self.output_widget, 0, 15, 8, 3)
        self.setCentralWidget(self.main_widget)

        self.left_label_2 = QtWidgets.QPushButton("功能实现")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("帮助")
        self.left_label_3.setObjectName('left_label')

        self.left_button_2 = QtWidgets.QPushButton("车流量检测")
        self.left_button_2.setObjectName('left_button')
        self.left_button_4 = QtWidgets.QPushButton("反馈建议")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton("联系我们")
        self.left_button_5.setObjectName('left_button')

        self.video_window = QtWidgets.QLabel("")
        self.video_window.setObjectName('video_window')

        listModel = QtCore.QStringListModel()
        listView = QtWidgets.QListView()
        items = ["使用说明:", "1:点击按钮“车流量检测”，在所弹出", "的对话框内选择将要测试的视频文件", "确认选择后，打开视频并执行车流量", "检测功能", "2:若要退出车流量检测功能，需先按", "ESC键，再点击车流量检测功能窗口","的关闭按钮，即可退出。"]

        listModel.setStringList(items)
        listView.setModel(listModel)




        #事件触发
        self.left_button_2.clicked.connect(self.function)


        self.left_layout.addWidget(self.left_label_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 8, 0, 1, 3)

        self.video_layout.addWidget(self.video_window,0,2,8,12)


        self.output_layout.addWidget(listView,0,15,8,6)

        self.left_widget.setStyleSheet('''
            QWidget{background:rgb(126,126,135)}
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700
        
            }
            QPushButton#left_button:hover{border-left:6px solid white;font-weight:700;}
        ''')
    def choose(self):
        videoName,filetype = QtWidgets.QFileDialog.getOpenFileName(self,"视频选择","./","All Files(*);;Video Files(*.mp4);;Video Files(*.avi)")
        if videoName:
            cur_path = QtCore.QDir('.')
            relative_path = cur_path.relativeFilePath(videoName)  #文件路径获取
            return relative_path






    def function(self):
        Trafficstatistics.main()



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())




if __name__ == '__main__' :
    main()

