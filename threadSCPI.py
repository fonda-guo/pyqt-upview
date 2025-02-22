from PyQt5.QtCore import *

from PCPoint import PCPoint, lookup_pointdict
from comPort import COM
import time

from comSCPI import SCPI

current = 0 #int16
def lookup_current():
    global current
    return current

def update_current_times10(cur):
    global current
    current = int(cur*10)

class Thread_SCPIHandle(QThread):
    faultACT = pyqtSignal(str)
    showLoad = pyqtSignal(float,float)
    vollowerbound = 2.7
    vollowerthd = 2.71
    tricklethreshould1 = 3.50    #78A
    tricklethreshould2 = 3.55    #31A
    volupperbound = 3.58

    def __init__(self):
        super(Thread_SCPIHandle, self).__init__()
        self.scpi = SCPI()
        self.pcpoint = PCPoint()
    def scpiCheckAct(self):
        if self.scpi.openFlag:
            result = ''
            try:
                result = self.scpi.actionPower.query('*IDN?')
            except:
                result = "Device opened but nothing responsed"
            return result
        else:
            return "Device not open"

    def volLoadQuery(self):
        if self.scpi.openFlag:
            try:
                result = self.scpi.actionPower.query('MEASure:VOLTage?')
            except:
                result = "Device opened but nothing responsed(vol)"
            return result
        else:
            return "Device not open(vol)"

    def currLoadQuery(self):
        if self.scpi.openFlag:
            try:
                result = self.scpi.actionPower.query('MEASure:CURRent?')
            except:
                result = "Device opened but nothing responsed(cur)"
            return result
        else:
            return "Device not open(cur)"

    def voltageSet(self,string):
        try:
            num = round(float(string),2)
        except:
            return -1
        if num < 0 or num > 50:
            return -1
        message = "SOUR:VOLT:DC " + str(num)
        self.scpi.writeSCPI(message)
        if str(num) != self.scpi.querySCPI("SOUR:VOLT:DC?"):
            return -2

    def loadCurSet(self,string):
        try:
            num = round(float(string), 2)
        except:
            return -1
        if num < 0 or num > 200:
            return -1
        message = "SOUR:CURR:NEG " + str(num)
        self.scpi.writeSCPI(message)
        if str(num) != self.scpi.querySCPI("SOUR:CURR:NEG?"):
            return -2

    def sourCurSet(self,string):
        try:
            num = round(float(string), 2)
        except:
            return -1
        if num < 0 or num > 200:
            return -1
        message = "SOUR:CURR:POS " + str(num)
        self.scpi.writeSCPI(message)
        if str(num) != self.scpi.querySCPI("SOUR:CURR:POS?"):
            return -2

    def output(self):
        if self.scpi.openFlag:
            self.scpi.writeSCPI("OUTP:STAT ON")
            return 0
        else:
            return -1

    def outputClose(self):
        if self.scpi.openFlag:
            self.scpi.writeSCPI("OUTP:STAT OFF")
            return 0
        else:
            return -1

    def run(self):
        while True:
            time.sleep(0.1)
            if self.scpi.openFlag:
                vol = self.volLoadQuery()
                cur = self.currLoadQuery()
                if vol == "Device opened but nothing responsed(vol)":
                    self.faultACT.emit(vol)
                    continue
                if cur == "Device opened but nothing responsed(cur)":
                    self.faultACT.emit(cur)
                    continue
                try:
                    vol = round(float(vol),2)
                except:
                    self.faultACT.emit("wrong vol number")
                    continue

                try:
                    cur = round(float(cur),2)
                except:
                    self.faultACT.emit("wrong cur number")
                    continue

                update_current_times10(cur)

                if vol >= 30 or vol <= 18:
                    self.faultACT.emit("vol fault")
                    self.outputClose()
                    continue

                if cur >= 200 or cur <= -200:
                    self.faultACT.emit("cur fault")
                    self.outputClose()
                    continue
                maxcellvol = float(lookup_pointdict(self.pcpoint.maxcellvol))
                mincellvol = float(lookup_pointdict(self.pcpoint.mincellvol))
                ts1 = float(lookup_pointdict(self.pcpoint.ts1))
                ts2 = float(lookup_pointdict(self.pcpoint.ts2))
                ts3 = float(lookup_pointdict(self.pcpoint.ts3))
                ts4 = float(lookup_pointdict(self.pcpoint.ts4))
                maxts = max(ts1,ts2,ts3,ts4)

                if maxts > 50:
                    self.faultACT.emit("over temperature fault!")
                    self.outputClose()
                if cur > 0:
                    #charge
                    if self.tricklethreshould1 < maxcellvol < self.tricklethreshould2:
                        if cur > 78:
                            self.sourCurSet("78")
                            self.faultACT.emit("trickle-charge mode 1 set(max 78A)")
                    elif self.tricklethreshould2 <= maxcellvol < self.volupperbound:
                        if cur > 31:
                            self.sourCurSet("31")
                            self.faultACT.emit("trickle-charge mode 2 set(max 31A)")
                    elif maxcellvol >= self.volupperbound:
                        self.sourCurSet("0")
                        self.faultACT.emit("upper cell voltage reached")
                        self.outputClose()
                if cur < 0:
                    #discharge
                    if self.vollowerbound < mincellvol <= self.vollowerthd:
                        if cur < -60:
                            self.loadCurSet("60")
                            self.faultACT.emit("discharge threthold reached(max 60A)")
                    elif mincellvol <= self.vollowerbound:
                        self.loadCurSet("0")
                        self.faultACT.emit("lower cell voltage reached")
                        self.outputClose()
                self.showLoad.emit(cur,vol)
