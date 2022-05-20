from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from processwindow import Ui_ProcessWindow


class ProcessWindow(QWidget, Ui_ProcessWindow):
    def __init__(self):
        super(ProcessWindow, self).__init__()
        self.setupUi(self)
        self.slot_init()

    def slot_init(self):
        self.pushButton.clicked.connect(self.close)