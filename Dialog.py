from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout


class Dialog(QDialog):

    def __init__(self, timeout, parent=None, classification="分类结果", confidence="0"):
        super(Dialog, self).__init__(parent)

        # 设置对话框的标题及大小
        self.setWindowTitle("分类结果")
        self.setWindowIcon(QIcon("static/checkmark.png"))
        self.resize(600, 200)
        self.layout = QHBoxLayout(self)
        self.label = QtWidgets.QLabel()
        self.label_classification = QtWidgets.QLabel()
        self.label_classification.setText(classification)
        self.label_confidence = QtWidgets.QLabel()
        self.label_confidence.setText(confidence)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label_classification)
        self.layout.addWidget(self.label_confidence)
        # 设置窗口为模态，用户只有关闭弹窗后，才能关闭主界面
        self.setWindowModality(Qt.ApplicationModal)
        self.time_to_wait = timeout
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        self.label.setText("窗口将在{0}秒后自动关闭...".format(self.time_to_wait-1))
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()