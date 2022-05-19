import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from mainwindow import Ui_MainWindow

import cv2
import numpy as np
from lib.Detector import Detector
from lib.trheads import DIThread,PIThread



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.detector = Detector()
        self.detector.load_model(r'E:\Git_repos\OrificeDetectionTool\snapshots\Net_epoch_150.pth')
        self.slot_init()

    def slot_init(self):
        """初始化按钮、动作和函数的连接"""
        self.pushButton.clicked.connect(self.detect_img)
        self.actionopen_file.triggered.connect(self.choose_file)
        self.actionopen_director.triggered.connect(self.process_imgs)
        self.actionload_model.triggered.connect(self.choose_model)

    # 以下为槽函数
    def detect_img(self):
        print("detecting")
        # 从label的pixmap提取图像
        imgptr = self.o_img.pixmap().toImage()
        ptr = imgptr.constBits()
        ptr.setsize(imgptr.byteCount())
        mat = np.array(ptr).reshape(imgptr.height(), imgptr.width(), 4)
        o_img = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)  # 得到cv格式的原始图片
        # 传到Thread
        self.diThread = DIThread(o_img, self.detector)
        self.diThread.start()
        self.diThread.trigger.connect(self.set_pixmap)
        print("detecting over")

    def process_imgs(self):
        fileName = QFileDialog.getExistingDirectory(self,
                                                              "选取文件",
                                                              "./"
                                                              )
        print("start scan folder")
        # 传到Thread
        self.piThread = PIThread(fileName,model=self.detector)
        self.piThread.start()
        print("over processing")

    def set_pixmap(self, img):
        img = img.convert("RGBA")
        data = img.tobytes("raw", "RGBA")
        qimg = QtGui.QImage(data, img.size[0], img.size[1], QtGui.QImage.Format_RGBA8888)
        r_img = QtGui.QPixmap.fromImage(qimg)
        self.r_img.setPixmap(r_img)  # 设置到r_img上
        self.r_img.setScaledContents(True)

    def choose_model(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         "选取文件",
                                                         "./",
                                                         "pth (*.pth)")  # 设置文件扩展名过滤,注意用双分号间隔
        self.detector.load_model(fileName)
        print('{}--load over'.format(fileName))

    def choose_file(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         "选取文件",
                                                         "./",
                                                         "jpg (*.jpg);;png (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔
        o_img = QtGui.QPixmap(fileName)
        self.o_img.setPixmap(o_img)
        self.o_img.setScaledContents(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
