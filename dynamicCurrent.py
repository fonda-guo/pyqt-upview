from PyQt5.QtCore import *
import pandas as pd
from PyQt5.QtWidgets import QFileDialog

from PCPoint import PCPoint, lookup_pointdict
import time


class dynamicCur(QObject):
    filename = ''
    index = 0
    totaltime = 0
    alreadypasttime = 0
    lastindextime = 0
    lasttimestamp = 0
    totalindex = 0
    dynamicCurTbl = pd.DataFrame()
    progressBarUpdate = pyqtSignal(int)
    indexlabelUpdate = pyqtSignal(float)
    def __init__(self):
        super().__init__()

    @staticmethod
    def analyzeFile():
        dynamicCur.dynamicCurTbl = pd.read_excel(dynamicCur.filename[0])
        dynamicCur.totalindex = dynamicCur.dynamicCurTbl.shape[0]
        for index,row in dynamicCur.dynamicCurTbl.iterrows():
            try:
                if row['Current'] < -160 or row["Current"] > 160:
                    return -1, "Wrong Current"
                elif row["Time"] < 0 or row["Time"] > 5000:
                    return -1, "Wrong Time"
                else:
                    dynamicCur.totaltime = dynamicCur.totaltime + row["Time"]
            except:
                return -1,"Wrong File Data Frame"
        return 1, "Data Analysis Finished"

    @staticmethod
    def clearParameter():
        dynamicCur.filename = ''
        dynamicCur.index = 0
        dynamicCur.totaltime = 0
        dynamicCur.alreadypasttime = 0
        dynamicCur.lastindextime = 0
        dynamicCur.lasttimestamp = 0
        dynamicCur.totalindex = 0
        dynamicCur.dynamicCurTbl = pd.DataFrame()
