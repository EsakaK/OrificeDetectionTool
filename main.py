import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from mainwindow import Ui_MainWindow
from video_object import VideoWindow
from process_object import ProcessWindow

import cv2
import numpy as np
from lib.Detector import Detector
from lib.trheads import DIThread, PIThread, EmittingStr


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.detector = Detector()
        self.detector.load_model(r'E:\Git_repos\OrificeDetectionTool\snapshots\Net_epoch_150.pth')
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        # sys.stderr = EmittingStr(textWritten=self.outputWritten)
        self.video_window = VideoWindow(self.detector)
        self.process_window = ProcessWindow()
        self.slot_init()

    def slot_init(self):
        """初始化按钮、动作和函数的连接"""
        self.pushButton.clicked.connect(self.detect_img)
        self.actionopen_file.triggered.connect(self.choose_file)
        self.actionopen_director.triggered.connect(self.process_imgs)
        self.actionload_model.triggered.connect(self.choose_model)
        # self.video_btn.clicked.connect(self.open_video_window)
        self.actionopen_video.triggered.connect(self.open_video_window)

    # 以下为辅助方法
    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    # 以下为槽函数
    def detect_img(self):
        print("detecting")
        # 从label的pixmap提取图像
        imgptr = self.o_img.pixmap().toImage()
        ptr = imgptr.constBits()
        ptr.setsize(imgptr.byteCount())
        mat = np.array(ptr).reshape(imgptr.height(), imgptr.width(), 4)
        o_img = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)  # 得到cv格式的原始RGB图片
        # 传到Thread
        self.diThread = DIThread(o_img, self.detector)
        self.diThread.start()
        self.diThread.trigger.connect(self.set_pixmap)
        print("detecting over.\n")

    def process_imgs(self):
        fileName = QFileDialog.getExistingDirectory(self,
                                                    "选取文件",
                                                    "./"
                                                    )
        if fileName != "":
            self.process_window.show()
            self.process_window.progressBar.setValue(0)
            print("start scan folder.")
            # 传到Thread
            self.piThread = PIThread(fileName, model=self.detector)
            self.piThread.start()
            self.piThread.trigger.connect(self.set_process_bar)


    def set_pixmap(self, img):
        img = img.convert("RGBA")
        data = img.tobytes("raw", "RGBA")
        qimg = QtGui.QImage(data, img.size[0], img.size[1], QtGui.QImage.Format_RGBA8888)
        r_img = QtGui.QPixmap.fromImage(qimg)
        self.r_img.setPixmap(r_img)  # 设置到r_img上
        self.r_img.setScaledContents(True)

    def set_process_bar(self,val):
        self.process_window.progressBar.setValue(val)

    def choose_model(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         "选取文件",
                                                         "./",
                                                         "pth (*.pth)")  # 设置文件扩展名过滤,注意用双分号间隔
        if fileName != "":
            self.detector.load_model(fileName)
            print('model "{}"--load over'.format(fileName))

    def choose_file(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         "选取文件",
                                                         "./",
                                                         "jpg (*.jpg);;png (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔
        if fileName != "":
            o_img = QtGui.QPixmap(fileName)
            self.o_img.setPixmap(o_img)
            self.o_img.setScaledContents(True)

    def open_video_window(self):
        self.video_window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
