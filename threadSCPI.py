from PyQt5.QtCore import *

from comPort import COM
import time

from comSCPI import SCPI

current = 0

class Thread_SCPIHandle(QThread):
    faultACT = pyqtSignal(str)
    showLoad = pyqtSignal(float,float)

    def __init__(self):
        super(Thread_SCPIHandle, self).__init__()
        self.scpi = SCPI()
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
            time.sleep(0.5)
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

                if vol >= 30 or vol <= 20:
                    self.faultACT.emit("vol fault")
                    self.outputClose()
                    continue

                if cur >= 200 or cur <= -200:
                    self.faultACT.emit("cur fault")
                    self.outputClose()
                    continue

                self.showLoad.emit(cur,vol)
