# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import csv
import time

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

import model
import utils
from Dialog import Dialog
from csv_utils import *
from model import classify_image, get_model_label


class Ui_MainWindow(object):

    def __init__(self, camera):
        self.camera = camera
        # Create a timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.start()

    def start(self):
        self.camera.openCamera()
        self.timer.start(1000. / 24)

    def nextFrameSlot(self):
        rval, frame = self.camera.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)

    def show_dialog(self):
        count_csv_path = "static/CSV/count.csv"  # 计数
        history_csv_path = "static/CSV/history.csv"  # 历史记录
        image_path = "static/photos/"  # 照片目录
        classification = "test"  # 测试用的

        timeout = 4 # 对话框停留时间
        ret, frame = self.camera.vc.read()  # 拍照
        self.history_photo_num = self.history_photo_num + 1  # 照片自增命名
        image_path = image_path + str(self.history_photo_num) + ".jpg"  # 保存照片的路径
        cv2.imwrite(image_path, frame)  # 保存
        # time.sleep(1)

        image = utils.load_image(image_path)
        classify_model = self.classify_model  # 模型、标签的初始化在setupUi函数最后
        label_to_content = self.label_to_content
        prediction, label = classify_image(image, classify_model) # 调用模型

        print('-' * 100)
        print(f'Test one image: {image_path}')
        print(f'classification: {label_to_content[str(label)]}\nconfidence: {prediction[0, label]}')
        print('-' * 100)

        classification = str(label_to_content[str(label)])  # 分类结果
        confidence = str(f'{prediction[0, label]}')  # 置信度
        confidence = confidence[0:5]  # 保留三位小数
        self.dialog = Dialog(timeout=timeout, classification=classification, confidence=confidence)  # 传入结果和置信度
        self.dialog.show()
        self.dialog.exec() # 对话框退出

        # 更新历史记录中count数目
        count_list = read_count_csv(filename=count_csv_path)
        count = int(count_list[0]) + 1
        self.count.setText(str(count))
        write_count_csv(filename=count_csv_path, count=count)

        # 更新历史记录
        write_history_csv(history_csv_path, classification=classification, photo_path=image_path)
        self.listWidget.clear()
        history_list = read_history_csv(history_csv_path)
        for record in history_list:  # 每次都是全部重新加载，效率较低...
            # self.listWidget.addItem(record[0])
            # print(record)
            item = QtWidgets.QListWidgetItem(QtGui.QIcon(record[1]), record[0])  # 0为类别，1为图片路径
            self.listWidget.addItem(item)

    def setupUi(self, MainWindow):
        count_csv_path = "static/CSV/count.csv"
        history_csv_path = "static/CSV/history.csv"
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 890)
        self.widget = QtWidgets.QWidget(MainWindow)
        self.widget.setObjectName("widget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(300, 240, 981, 651))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.videoLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.videoLayout.setContentsMargins(0, 0, 0, 0)
        self.videoLayout.setObjectName("videoLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.videoLayout.addWidget(self.label)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 298, 238))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.calendarLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.calendarLayout.setContentsMargins(0, 0, 0, 0)
        self.calendarLayout.setObjectName("calendarLayout")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.horizontalLayoutWidget_2)
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarLayout.addWidget(self.calendarWidget)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(299, 0, 982, 241))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.logoLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.logoLayout.setContentsMargins(0, 0, 0, 0)
        self.logoLayout.setObjectName("logoLayout")
        self.logo = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("static/logo.png"))
        self.logo.setObjectName("logo")
        self.logoLayout.addWidget(self.logo)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(90, 240, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_dialog)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 510, 301, 381))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.listLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.listLayout.setContentsMargins(0, 0, 0, 0)
        self.listLayout.setObjectName("listLayout")
        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget_2)
        self.listWidget.setObjectName("listWidget")
        self.listLayout.addWidget(self.listWidget)
        self.tip = QtWidgets.QLabel(self.widget)
        self.tip.setGeometry(QtCore.QRect(10, 270, 281, 161))
        self.tip.setWordWrap(True)
        self.tip.setObjectName("tip")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(0, 470, 301, 41))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.historyLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.historyLayout.setContentsMargins(0, 0, 0, 0)
        self.historyLayout.setObjectName("historyLayout")
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.label_4.setObjectName("label_4")
        self.historyLayout.addWidget(self.label_4)
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(-1, 429, 301, 41))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.countLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.countLayout.setContentsMargins(0, 0, 0, 0)
        self.countLayout.setObjectName("countLayout")
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        self.label_5.setObjectName("label_5")
        self.countLayout.addWidget(self.label_5)
        self.count = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        self.count.setText("")
        self.count.setObjectName("count")
        self.countLayout.addWidget(self.count)
        MainWindow.setCentralWidget(self.widget)

        # 加载模型
        classify_model, label_to_content = get_model_label()
        self.classify_model = classify_model
        self.label_to_content = label_to_content

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 加载计数
        count_list = read_count_csv(filename=count_csv_path)
        self.count.setText(str(count_list[0]))

        # 照片编号
        self.history_photo_num = int(count_list[0])

        # 加载历史记录
        history_list = read_history_csv(history_csv_path)
        for record in history_list:
            # self.listWidget.addItem(record[0])
            # print(record)
            item = QtWidgets.QListWidgetItem(QtGui.QIcon(record[1]), record[0])
            self.listWidget.addItem(item)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.tip.setText(_translate("MainWindow", "使用方法：将垃圾放在翻转盖板上,摄像头将对垃圾拍照；分类模型根据照片对垃圾进行二分类；树莓派根据分类结果控制舵机将垃圾进行分类。"))
        self.label_4.setText(_translate("MainWindow", "最近历史记录："))
        self.label_5.setText(_translate("MainWindow", "共分类次数："))
