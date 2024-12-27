import csv
import time

from PyQt5.QtCore import *
from PCPoint import PCPoint, lookup_pointdict


class Thread_DataSaveHandle(QThread):
    fileNameShow = pyqtSignal(str)
    def __init__(self):
        super(Thread_DataSaveHandle, self).__init__()
        self.pcdict = PCPoint()
        self.cell1VolSave = 0
        self.cell2VolSave = 0
        self.cell3VolSave = 0
        self.cell4VolSave = 0
        self.cell5VolSave = 0
        self.cell6VolSave = 0
        self.cell7VolSave = 0
        self.cell8VolSave = 0
        self.stackVolSave = 0
        self.ts1Save = 0
        self.ts2Save = 0
        self.ts3Save = 0
        self.ts4Save = 0
        self.currentSave = 0
        self.writeFlag = False
        self.savePCDict = {
            "time"     : -1,
            "cell1Vol" : self.pcdict.cell1Vol,
            "cell2Vol" : self.pcdict.cell2Vol,
            "cell3Vol" : self.pcdict.cell3Vol,
            "cell4Vol" : self.pcdict.cell4Vol,
            "cell5Vol" : self.pcdict.cell5Vol,
            "cell6Vol" : self.pcdict.cell6Vol,
            "cell7Vol" : self.pcdict.cell7Vol,
            "cell8Vol" : self.pcdict.cell8Vol,
            "stackVol" : self.pcdict.stackVol,
            "ts1" : self.pcdict.ts1,
            "ts2" : self.pcdict.ts2,
            "ts3" : self.pcdict.ts3,
            "ts4" : self.pcdict.ts4,
            "current" : self.pcdict.current,
            "SOC_box" : self.pcdict.SOC_box,
            "SOC_cell1" : self.pcdict.SOC_cell1,
            "SOC_cell2" : self.pcdict.SOC_cell2,
            "SOC_cell3" : self.pcdict.SOC_cell3,
            "SOC_cell4" : self.pcdict.SOC_cell4,
            "SOC_cell5" : self.pcdict.SOC_cell5,
            "SOC_cell6" : self.pcdict.SOC_cell6,
            "SOC_cell7" : self.pcdict.SOC_cell7,
            "SOC_cell8" : self.pcdict.SOC_cell8
        }
        self.filename = "./data" + time.strftime('%Y-%m-%d %H-%M-%S') + ".csv"
        self.nameRow = []
        for key in self.savePCDict:
            self.nameRow.append(key)
        self.newDataFile()

    def newDataFile(self):
        self.filename = "./data/" + time.strftime('%Y-%m-%d %H-%M-%S') + ".csv"
        with open(self.filename, 'w', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(self.nameRow)

    def stopSave(self):
        self.writeFlag = False

    def startSave(self):
        self.writeFlag = True

    def run(self):
        while True:
            time.sleep(1)
            if self.writeFlag:
                num2write = []
                for key in self.savePCDict:
                    if key == "time":
                        timestamp = time.time()
                        num2write.append(str(timestamp))
                    else:
                        num2write.append(lookup_pointdict(self.savePCDict[key]))
                with open(self.filename, 'a', newline = '') as f:
                    writer = csv.writer(f)
                    writer.writerow(num2write)
                self.fileNameShow.emit(self.filename)
