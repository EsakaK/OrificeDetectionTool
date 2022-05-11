import sys
import random
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def open_file(self):


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())