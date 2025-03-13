from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog

from dynamicCurrent import dynamicCur


class Thread_DynamicFile(QThread):
    analyzeStateSig = pyqtSignal(int, str)
    def __init__(self):
        super().__init__()
    def run(self):
        dynamicCur.clearParameter()
        dynamicCur.filename = QFileDialog.getOpenFileName(None, 'Open File', '.')
        if dynamicCur.filename:
            bit, message = dynamicCur.analyzeFile()
            self.analyzeStateSig.emit(bit,message)
