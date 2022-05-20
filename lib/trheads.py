import os
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread,QObject
import numpy as np
from PIL import Image
import cv2


class DIThread(QThread):
    """用于检测单个图片的线程"""
    trigger = pyqtSignal(Image.Image)

    def __init__(self, img, model):
        super(DIThread, self).__init__()
        self.o_img = img
        self.model = model

    def run(self):
        r_img = self.model.write_frame(self.o_img)
        r_img = Image.fromarray(r_img)
        self.trigger.emit(r_img)
        print('emit over')


class PIThread(QThread):
    """用于处理文件夹所有文件的线程"""

    def __init__(self, path, model):
        super(PIThread, self).__init__()
        self.path = path
        self.model = model

    def run(self):
        file_list = os.listdir(path=self.path)
        print(self.path)
        for file in file_list:
            if ".jpg" in file:
                img = cv2.imread(os.path.join(self.path,file),cv2.IMREAD_COLOR)
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                out_img = self.model.write_frame(img)
                out_img = Image.fromarray(out_img)

                dir = os.path.join(self.path,'result')  # 想要保存的路径
                if not os.path.exists(dir):  # 如果不存在路径，则创建这个路径，关键函数就在这两行，其他可以改变
                    os.makedirs(dir)

                out_img.save(os.path.join(dir,file))


class EmittingStr(QObject):
    textWritten = pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))