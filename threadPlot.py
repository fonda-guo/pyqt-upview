import time

from PyQt5.QtCore import *

from PCPoint import lookup_pointdict, PCPoint


class Thread_PlotHandle(QThread):
    dataFinished = pyqtSignal()
    def __init__(self):
        super(Thread_PlotHandle, self).__init__()
        self.t_cur = [0]
        self.t_vol = [0]
        self.voltage = [0]
        self.current = [0]
        self.openPlotFlag = False
        self.pcpoint = PCPoint()
        self.voltageIndexDict = {"Cell 1 voltage": self.pcpoint.cell1Vol,
                                 "Cell 2 voltage": self.pcpoint.cell2Vol,
                                 "Cell 3 voltage": self.pcpoint.cell3Vol,
                                 "Cell 4 voltage": self.pcpoint.cell4Vol,
                                 "Cell 5 voltage": self.pcpoint.cell5Vol,
                                 "Cell 6 voltage": self.pcpoint.cell6Vol,
                                 "Cell 7 voltage": self.pcpoint.cell7Vol,
                                 "Cell 8 voltage": self.pcpoint.cell8Vol}
        self.voltageIndex = self.voltageIndexDict["Cell 1 voltage"]

    def updateVoltageIndex(self,string):
        self.voltageIndex = self.voltageIndexDict[string]

    def updateData(self,t,oldList,newdata):
        if len(t) < 60:
            t.append(t[-1] + 1)
            oldList.append(newdata)
        elif len(t) >= 60 :
            t = t[1:]
            t.append(t[-1] + 1)
            oldList = oldList[1:]
            oldList.append(newdata)
        return t,oldList

    def run(self):
        while True:
            time.sleep(1)
            if self.openPlotFlag:
                cur = float(lookup_pointdict(self.pcpoint.current))
                vol = float(lookup_pointdict(self.voltageIndex))
                self.t_cur,self.current = self.updateData(self.t_cur, self.current, cur)
                self.t_vol,self.voltage = self.updateData(self.t_vol, self.voltage, vol)
                self.dataFinished.emit()


