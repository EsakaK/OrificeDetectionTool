from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from videowindow import Ui_VideoWindow
from lib.trheads import DIThread

import cv2
import os
from PIL import Image


class VideoWindow(QWidget, Ui_VideoWindow):
    def __init__(self,detector):
        super(VideoWindow, self).__init__()
        self.setupUi(self)
        self.timer_camera = QtCore.QTimer()
        self.frame_s = 3
        self.frame_gap = 3
        self.detector = detector
        self.slot_init()

    def slot_init(self):
        self.open_video.clicked.connect(self.open_video_button)
        self.btn1.clicked.connect(self.detect_video)
        self.timer_camera.timeout.connect(self.show_camera_up)
        self.timer_camera.timeout.connect(self.show_camera_down)

    # 打开视频
    def open_video_button(self):
        if self.timer_camera.isActive() == False:

            imgName, imgType = QFileDialog.getOpenFileName(self, "打开视频", "", "*.mp4;;*.AVI;;*.rmvb;;All Files(*)")

            self.cap_video = cv2.VideoCapture(imgName)

            flag = self.cap_video.isOpened()

            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请提供正确的视频格式",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)

            else:

                # self.timer_camera3.start(30)
                self.show_camera_up()
                self.open_video.setText(u'关闭视频')
        else:
            self.cap_video.release()
            self.label_show_camera.clear()
            self.timer_camera.stop()
            self.frame_s = self.frame_gap
            self.label_show_camera1.clear()
            self.open_video.setText(u'打开视频')

    # 检测视频
    def detect_video(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap_video.isOpened()
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请提供正确的视频格式",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)

            else:
                self.timer_camera.start(30)

        else:
            self.timer_camera.stop()
            self.cap_video.release()
            self.label_show_camera1.clear()

        # 显示上面的视频
    def show_camera_up(self):
        # 抽帧
        length = int(self.cap_video.get(cv2.CAP_PROP_FRAME_COUNT))  # 抽帧
        flag, self.image1 = self.cap_video.read()  # image1是视频的
        if flag == True:
            if self.frame_s % self.frame_gap == 0:  # 抽帧

                dir_path = os.getcwd()
                # print("dir_path",dir_path)
                #camera_source = dir_path + "\\tmp.jpg"

                #cv2.imwrite(camera_source, self.image1)

                width = self.image1.shape[1]
                height = self.image1.shape[0]

                # 设置新的图片分辨率框架
                width_new = 640
                height_new = 360

                # 判断图片的长宽比率
                if width / height >= width_new / height_new:

                    show = cv2.resize(self.image1, (width_new, int(height * width_new / width)))
                else:

                    show = cv2.resize(self.image1, (int(width * height_new / height), height_new))

                show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)

                showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], 3 * show.shape[1],
                                         QtGui.QImage.Format_RGB888)

                self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        else:
            self.cap_video.release()
            self.label_show_camera.clear()
            self.timer_camera.stop()

            self.label_show_camera1.clear()
            self.open_video.setText(u'打开视频')

    # 显示视频下面
    def show_camera_down(self):

        flag, self.image1 = self.cap_video.read()
        self.frame_s += 1
        if flag == True:
            if self.frame_s % self.frame_gap == 0:  # 抽帧

                dir_path = os.getcwd()
                #camera_source = dir_path + "\\tmp.jpg"

                #cv2.imwrite(camera_source, self.image1)
                # 传入计算
                self.image1 = cv2.cvtColor(self.image1,cv2.COLOR_BGR2RGB)
                img = self.detector.write_frame(self.image1)
                width = img.shape[1]
                height = img.shape[0]

                # 设置新的图片分辨率框架
                width_new = 640
                height_new = 360

                # 判断图片的长宽比率
                if width / height >= width_new / height_new:

                    show = cv2.resize(img, (width_new, int(height * width_new / width)))
                else:

                    show = cv2.resize(img, (int(width * height_new / height), height_new))

                showImage = QtGui.QImage(show, show.shape[1], show.shape[0], 3 * show.shape[1],
                                         QtGui.QImage.Format_RGB888)

                self.label_show_camera1.setPixmap(QtGui.QPixmap.fromImage(showImage))