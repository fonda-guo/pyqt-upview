import sys

from userMainWindow import MainWindow, Ui_UserMainWindow
from Commu_test import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    u = Ui_UserMainWindow(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())


