import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from Camera import Camera
from Window import Ui_MainWindow


if __name__ == "__main__":
    camera = Camera(1)
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow(camera)
    ui.setupUi(window)
    window.setWindowTitle("智慧垃圾分类系统")
    window.setWindowIcon(QIcon("static/recycle-bin.png"))
    window.show()
    sys.exit(app.exec_())

