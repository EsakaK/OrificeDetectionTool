import sys
import random
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot
from mainwindow import Ui_MainWindow

import cv2


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.slot_init()

    def slot_init(self):
        """初始化按钮、动作和函数的连接"""
        self.ui.pushButton.clicked.connect(self.on_click)
        self.ui.actionopen_file.triggered.connect(self.choose_file)

    @pyqtSlot()
    def on_click(self):
        print("检测中")

    @pyqtSlot()
    def choose_file(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         "选取文件",
                                                         "./",
                                                         "jpg (*.jpg);;png (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔
        o_img = QtGui.QPixmap(fileName)
        self.ui.o_img.setPixmap(o_img)
        self.ui.o_img.setScaledContents(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
