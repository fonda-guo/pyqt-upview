import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLCDNumber

import Commu_test
from Commu_test import *
from threadSCPI import Thread_SCPIHandle
from threadSerial import Thread_SerialHandle


class Ui_UserMainWindow(Ui_MainWindow):
    def __init__(self,MainWindow):
        self.setupUi(MainWindow)
        self.displayInit()
    # Object serial
        self.thread_Serial = Thread_SerialHandle()
        self.thread_Serial.data_received.connect(self.readData)
        self.thread_Serial.showbatdata.connect(self.showBatData)
        self.thread_Serial.start()
        self.thread_Serial.data_lost.connect(self.dataWrongReport)

        self.thread_scpi = Thread_SCPIHandle()
        self.thread_scpi.start()
        self.thread_scpi.faultACT.connect(self.wrongMessage)
        self.thread_scpi.showLoad.connect(self.showLoadData)

        self.showdict = {0:self.lcdcell1,
                         1:self.lcdcell2,
                         2:self.lcdcell3,
                         3:self.lcdcell4,
                         4:self.lcdcell5,
                         5:self.lcdcell6,
                         6:self.lcdcell7,
                         7:self.lcdcell8,
                         8:self.lcdcell9,
                         9:self.lcdcell10,
                         10:self.lcdcell11,
                         11:self.lcdcell12,
                         12:self.lcdcell13,
                         13:self.lcdcell14,
                         14:self.lcdcell15,
                         15:self.lcdcell16,
                         16:self.lcdstack,
                         17:self.lcdLDpin,
                         18:self.lcdcellab,
                         19:self.lcdcellssA,
                         20:self.lcdcellssB,
                         21:self.lcdcellssC,
                         22:self.lcdcellfs,
                         23:self.lcdcellTS1,
                         24:self.lcdcellTS2,
                         25:self.lcdcellTS3,
                         26:self.lcdcellTS4,
                         27:self.lcdcurrent,
                         28:self.lcdcnter
                         }


    def displayInit(self):
        self.pushButton_scanport.clicked.connect(self.scanPort)
        self.pushButton_openport.clicked.connect(self.openclosePort)
        self.pushButton_sendmessage.clicked.connect(self.sendMessage)
        self.pushButton_clearinfo.clicked.connect(self.clearInfoWindow)
        self.pushButton_clearmessage.clicked.connect(self.clearMessageWindow)
        self.pushButton_openAct.clicked.connect(self.openAct)
        self.pushButton_checkAct.clicked.connect(self.checkAct)
        self.pushButton_writeAct.clicked.connect(self.writeAct)
        self.pushButton_queryAct.clicked.connect(self.queryAct)
        self.pushButton_sendhex.clicked.connect(self.sendHexMessage)
        self.pushButton_clearcnter.clicked.connect(self.testcnterClear)
        self.pushButton_clearBatInfo.clicked.connect(self.batInfoClear)
        self.pushButton_volSet.clicked.connect(self.volSetAct)
        self.pushButton_loadCurSet.clicked.connect(self.loadCurSetAct)
        self.pushButton_sourCurSet.clicked.connect(self.sourCurSetAct)
        self.pushButton_clearSCPIinfo.clicked.connect(self.clearSCPIinfo)
        self.pushButton_outputACT.clicked.connect(self.outputACT)
   # serial
    def scanPort(self):
        self.comboBox_com.clear()
        myport = self.thread_Serial.comPort.list_port()
        if myport == "None":
            self.comboBox_com.addItem("None")
        else:
            for port in myport:
                self.comboBox_com.addItem(port.name)

    def openclosePort(self):
        comname = self.comboBox_com.currentText()
        if comname == "None" or comname == "":
            return
        comrate = self.comboBox_rate.currentText()
        if self.pushButton_openport.text() == 'open port':
            if self.thread_Serial.comPort.openFlag: return
            self.thread_Serial.comPort.openComPort(comname,comrate)
            self.pushButton_openport.setText("close port")
        else:
            self.thread_Serial.comPort.openFlag = False
            self.thread_Serial.comPort.closeComPort()
            self.pushButton_openport.setText("open port")
    # send Str
    def sendMessage(self):
        message = self.textEdit_sendmessage.toPlainText()
        num = self.thread_Serial.comPort.writeComPort(message.encode())
        self.textEdit_sendmessage.clear()
        self.textBrowser_info.insertPlainText("Should send:"+str(len(message))+". Actually send: " + str(num)+";\n")
    # send HEX message
    def sendHexMessage(self):
        hexmessage = self.textEdit_sendhex.toPlainText()
        bytemessage = bytes.fromhex(hexmessage)
        num = self.thread_Serial.comPort.writeComPort(bytemessage)
        self.textEdit_sendhex.clear()
        self.textBrowser_info.insertPlainText(
            "Should send:" + str(len(bytemessage)) + ". Actually send: " + str(num) + ";\n")
    def readData(self,m):
        if self.comboBox_recevie.currentText() == "String":
            try:
                self.textBrowser_receive.append(str(m.decode('utf-8')))
            except:
                self.textBrowser_receive.append("not right string type")
        else:
          self.textBrowser_receive.append(m.hex())

    def clearInfoWindow(self):
        self.textBrowser_info.clear()

    def clearMessageWindow(self):
        self.textBrowser_receive.clear()
    # open load
    def openAct(self):
        meassage = self.thread_scpi.scpi.openSCPI()
        self.textBrowser_info_ACT.append(meassage)
    def checkAct(self):
        self.textBrowser_info_ACT.append(self.thread_scpi.scpiCheckAct())

    def clearSCPIinfo(self):
        self.textBrowser_info_ACT.clear()

    def writeAct(self):
        if self.thread_scpi.scpi.openFlag:
            message = self.textEdit_writeAct.toPlainText()
            self.thread_scpi.scpi.writeSCPI(message)
    def queryAct(self):
        if self.thread_scpi.scpi.openFlag:
            message = self.textEdit_queryAct.toPlainText()
            result = ""
            try:
                result = self.thread_scpi.scpi.querySCPI(message)
            except:
                reslut = "something went wrong"
            self.textBrowser_queryACTBack.setText(result)

    def volSetAct(self):
        res = self.thread_scpi.voltageSet(self.textEdit_volSet.toPlainText())
        if res == -1:
            self.textBrowser_info_ACT.append("wrong voltage number!")
        elif res == -2:
            self.textBrowser_info_ACT.append("voltage set fail!")

    def loadCurSetAct(self):
        res = self.thread_scpi.loadCurSet(self.textEdit_loadCurSet.toPlainText())
        if res == -1:
            self.textBrowser_info_ACT.append("wrong load cur number!")
        elif res == -2:
            self.textBrowser_info_ACT.append("load cur set fail!")

    def sourCurSetAct(self):
        res = self.thread_scpi.sourCurSet(self.textEdit_sourCurSet.toPlainText())
        if res == -1:
            self.textBrowser_info_ACT.append("wrong sour cur number!")
        elif res == -2:
            self.textBrowser_info_ACT.append("sour cur set fail!")

    def outputACT(self):
        if self.pushButton_outputACT.text() == "ACT Output":
            if self.thread_scpi.output() == 0:
                self.pushButton_outputACT.setText("Close Output")
        elif self.pushButton_outputACT.text() == "Close Output":
            if self.thread_scpi.outputClose() == 0:
                self.pushButton_outputACT.setText("ACT Output")

    def wrongMessage(self,string):
        self.textBrowser_info_ACT.append(string)

    def showLoadData(self,cur,vol):
        self.textBrowser_info_ACTcur.setText(str(cur))
        self.textBrowser_info_ACTvol.setText(str(vol))


    # def showBatData(self,index,data):
    def showBatData(self,index,data):
        if (index >= 0) and (index <= self.thread_Serial.PCPoint.LDpinVol):
            self.showdict[index].display(format(data/1000, '.3f'))
        elif index <= self.thread_Serial.PCPoint.fet_Status:
            self.showdict[index].setHexMode()
            self.showdict[index].display(data)
        elif index <= self.thread_Serial.PCPoint.ts4:
            self.showdict[index].display(format(data/10, '.1f'))
        elif index == self.thread_Serial.PCPoint.current:
            self.showdict[index].display(format(data/25, '.1f'))
        elif index ==self.thread_Serial.PCPoint.test_cnter:
            hour = int(data*0.5/3600)
            minute = int(data*0.5/60)  - hour*60
            second = data*0.5 - hour*3600 - minute*60
            self.showdict[index].display(str(hour)+':'+str(minute)+':'+str(format(second, '.1f')))
        elif index == self.thread_Serial.PCPoint.fault:
            if data == 1:
                self.textBrowser_batInfo.append("I2C DEAD!")

    def dataWrongReport(self):
        self.textBrowser_info.append("packet lost!")

    def testcnterClear(self):
        self.thread_Serial.comPort.writeComPort(bytes.fromhex("0701001C0000000A"))

    def batInfoClear(self):
       self.textBrowser_batInfo.clear()


##############################################################
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.fuction = None



