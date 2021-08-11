import cv2
from PyQt5.QtWidgets import QMessageBox


class Camera:

    def __init__(self, camera):
        self.vc = cv2.VideoCapture(camera)


    def openCamera(self):
        # self.vc = cv2.VideoCapture(1)
        # vc.set(5, 30)  #set FPS
        self.vc.set(3, 1100)  # set width
        self.vc.set(4, 960)  # set height

        if not self.vc.isOpened():
            print('failure')
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return

    # def initialize(self):
    #     self.cap = cv2.VideoCapture(self.camera)
