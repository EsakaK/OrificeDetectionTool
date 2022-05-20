from PyQt5.QtWidgets import QMainWindow, QWidget
from videowindow import Ui_VideoWindow


class VideoWindow(QWidget, Ui_VideoWindow):
    def __init__(self):
        super(VideoWindow, self).__init__()
        self.setupUi(self)
