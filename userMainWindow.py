import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLCDNumber
from pyexpat.errors import messages

import Commu_test
from Commu_test import *
from PCPoint import update_pointdict, lookup_pointdict
from threadDataSave import Thread_DataSaveHandle
from threadPlot import Thread_PlotHandle
from threadSCPI import Thread_SCPIHandle
from threadSerial import Thread_SerialHandle
import pyqtgraph as pg


class Ui_UserMainWindow(Ui_MainWindow):
    def __init__(self,MainWindow):
        self.setupUi(MainWindow)
        self.myPen = pg.mkPen(color=(255, 0, 0),width = 2.5)
        self.displayInit()
    # Object serial
        self.thread_Serial = Thread_SerialHandle()
        self.thread_Serial.data_received.connect(self.readData)
        self.thread_Serial.showbatdata.connect(self.showBatData)
        self.thread_Serial.data_lost.connect(self.dataWrongReport)
        self.thread_Serial.start()


        self.thread_scpi = Thread_SCPIHandle()
        self.thread_scpi.faultACT.connect(self.wrongMessage)
        self.thread_scpi.showLoad.connect(self.showLoadData)
        self.thread_scpi.start()

        self.thread_save = Thread_DataSaveHandle()
        self.thread_save.fileNameShow.connect(self.showFileName)
        self.thread_save.start()

        #plot
        self.thread_plot = Thread_PlotHandle()
        self.thread_plot.dataFinished.connect(self.plotUpdate)
        self.thread_plot.start()

        self.debugBuffer = 0

        self.showdict = {0:self.lcdcell1,
                         1:self.lcdcell2,
                         2:self.lcdcell3,
                         3:self.lcdcell4,
                         4:self.lcdcell5,
                         5:self.lcdcell6,
                         6:self.lcdcell7,
                         7:self.lcdcell8,
                         8:self.lcdstack,
                         9:self.lcdLDpin,
                         10:self.lcdcellab,
                         11:self.lcdcellssA,
                         12:self.lcdcellssB,
                         13:self.lcdcellssC,
                         14:self.lcdcellfs,
                         15:self.lcdcellTS1,
                         16:self.lcdcellTS2,
                         17:self.lcdcellTS3,
                         18:self.lcdcellTS4,
                         19:self.lcdcurrent,
                         20:self.lcdcnter,
                         23:self.lcdSOCbox,
                         24:self.lcdSOCcell1,
                         25:self.lcdSOCcell2,
                         26:self.lcdSOCcell3,
                         27:self.lcdSOCcell4,
                         28:self.lcdSOCcell5,
                         29:self.lcdSOCcell6,
                         30:self.lcdSOCcell7,
                         31:self.lcdSOCcell8,
                         32:self.lcdSOHbox,
                         35:self.lcdR1,
                         36:self.lcdR2,
                         37:self.lcdR3,
                         38:self.lcdR4,
                         39:self.lcdR5,
                         40:self.lcdR6,
                         41:self.lcdR7,
                         42:self.lcdR8,
                         43:self.lcddVdC1,
                         44:self.lcddVdC2,
                         45:self.lcddVdC3,
                         46:self.lcddVdC4,
                         47:self.lcddVdC5,
                         48:self.lcddVdC6,
                         49:self.lcddVdC7,
                         50:self.lcddVdC8,
                         51:self.lcdCBbits,
                         53:self.lcdSOCbox_Cal,
                         54:self.lcdSOCbox_Show
                         }

        self.CBshowdict = {
                          0:self.CB_cell1,
                          1:self.CB_cell2,
                          2:self.CB_cell3,
                          3:self.CB_cell4,
                          4:self.CB_cell5,
                          5:self.CB_cell6,
                          14:self.CB_cell7,
                          15:self.CB_cell8
                          }

        self.CellCalishowdict = {
                          0: self.CB_cell1_cali,
                          1: self.CB_cell2_cali,
                          2: self.CB_cell3_cali,
                          3: self.CB_cell4_cali,
                          4: self.CB_cell5_cali,
                          5: self.CB_cell6_cali,
                          6: self.CB_cell7_cali,
                          7: self.CB_cell8_cali
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
        self.pushButton_newFileSave.clicked.connect(self.newDataSave)
        self.pushButton_StartSave.clicked.connect(self.startStopSavingData)
        self.pushButton_sendAddr.clicked.connect(self.sendDebugAddr)
        self.comboBox_plotcellchose.currentIndexChanged.connect(self.cellVoltageIndexUpdate)
        self.pushButton_CBcontrol.clicked.connect(self.closeOpneCB)
        self.pushButton_cutOffCur.clicked.connect(self.cutOffCur)
        #limit or window will cursh after 6 hours
        self.textBroswerMaxSet()
        #plot init
        self.mycurPlot = self.plotCurrentInit()
        self.myvolPlot = self.plotVoltageInit()
   #all textBroswer max 20 message
    def textBroswerMaxSet(self):
        self.textBrowser_receive.document().setMaximumBlockCount(20)
        self.textBrowser_batInfo.document().setMaximumBlockCount(20)
        self.textBrowser_info.document().setMaximumBlockCount(20)
        self.textBrowser_info_ACT.document().setMaximumBlockCount(20)
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
            self.plotClear()
            self.thread_plot.openPlotFlag = True  #start plot
        else:
            self.thread_Serial.comPort.openFlag = False
            self.thread_Serial.comPort.closeComPort()
            self.pushButton_openport.setText("open port")
            self.thread_plot.openPlotFlag = False  #end plot
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

    def cutOffCur(self):
        if self.pushButton_cutOffCur.text() == "Cutoff Cur":
            self.thread_Serial.cutOffCur = True
            self.pushButton_cutOffCur.setText("Recover Cur")
        elif self.pushButton_cutOffCur.text() == "Recover Cur":
            self.thread_Serial.cutOffCur = False
            self.pushButton_cutOffCur.setText("Cutoff Cur")


    # def showBatData(self,index,data):
    def showBatData(self,index,data):
        if (index >= 0) and (index <= self.thread_Serial.PCPoint.LDpinVol):
            self.showdict[index].display(format(data/1000, '.3f'))
        elif index <= self.thread_Serial.PCPoint.fet_Status:
            self.showdict[index].setHexMode()
            self.showdict[index].display(data)
        elif index <= self.thread_Serial.PCPoint.ts4:
            if data > 32767:
                data = data - 65536
            self.showdict[index].display(format(data/10, '.1f'))
        elif index == self.thread_Serial.PCPoint.current:

            #self.showdict[index].display(format((int(data))/25, '.1f'))
            #int16 show:
            show_cur = data
            if data > 32767:
                show_cur = data - 65536
            #self.showdict[index].display(format(show_cur/ 25, '.1f'))
            self.showdict[index].display(format(show_cur / 10, '.1f'))
        elif index ==self.thread_Serial.PCPoint.test_cnter:
            hour = int(data*0.5/3600)
            minute = int(data*0.5/60)  - hour*60
            second = data*0.5 - hour*3600 - minute*60
            self.showdict[index].display(str(hour)+':'+str(minute)+':'+str(format(second, '.1f')))
        elif index == self.thread_Serial.PCPoint.debug_register1:
            self.debugBuffer = data
        elif index == self.thread_Serial.PCPoint.debug_register2:
            self.debugBuffer = (self.debugBuffer << 16) + data
            self.textBrowser_DebugReg.setText(hex(self.debugBuffer))
        elif self.thread_Serial.PCPoint.SOC_box <= index <= self.thread_Serial.PCPoint.SOH_box:
            self.showdict[index].display(format(data/100, '.2f'))
        elif self.thread_Serial.PCPoint.resis_cell1 <= index <= self.thread_Serial.PCPoint.resis_cell8:
            self.showdict[index].display(format(data/1000, '.3f'))
        elif self.thread_Serial.PCPoint.dVdC1 <= index <= self.thread_Serial.PCPoint.dVdC8:
            self.showdict[index].display(format(data, '.0f'))
        elif index == self.thread_Serial.PCPoint.CB_bits:
            self.showCBStatus(data)
        elif index == self.thread_Serial.PCPoint.SOC_box_cal or index == self.thread_Serial.PCPoint.SOC_box_show:
            self.showdict[index].display(format(data / 100, '.2f'))
        elif index == self.thread_Serial.PCPoint.Cali_bits:
            self.showCaliStatus(data)
        elif index == self.thread_Serial.PCPoint.fault:
            if data == 1:
                self.textBrowser_batInfo.append("I2C DEAD!")

    def showCaliStatus(self,Cali_Bits):
        for key in self.CellCalishowdict:
            if ((1<<key) & Cali_Bits) != 0:
                self.CellCalishowdict[key].setStyleSheet("background-color:rgb(255, 0, 0)")
            else:
                self.CellCalishowdict[key].setStyleSheet("background-color:rgb(255, 255, 255)")

    def dataWrongReport(self):
        self.textBrowser_info.append("packet lost!")

    def testcnterClear(self):
        message = self.thread_Serial.PCPoint.writePointData(self.thread_Serial.PCPoint.test_cnter,0)
        self.thread_Serial.comPort.writeComPort(message)

    def batInfoClear(self):
       self.textBrowser_batInfo.clear()

    #Save Data
    def showFileName(self,fileName):
        self.textBrowser_FileName.setText(fileName)

    def newDataSave(self):
        self.thread_save.newDataFile()

    def startStopSavingData(self):
        text = self.pushButton_StartSave.text()
        if text == "Start Saving Data":
            self.thread_save.writeFlag = True
            self.pushButton_StartSave.setText("Stop Saving Data")
        elif text == "Stop Saving Data":
            self.thread_save.writeFlag = False
            self.pushButton_StartSave.setText("Start Saving Data")

##Cell Balance
    def showCBStatus(self,CB_Bits):
        for key in self.CBshowdict:
            if ((1<<key) & CB_Bits) != 0:
                self.CBshowdict[key].setStyleSheet("background-color:rgb(0, 255, 0)")
            else:
                self.CBshowdict[key].setStyleSheet("background-color:rgb(255, 255, 255)")

    def  closeOpneCB(self):
        if self.pushButton_CBcontrol.text() == 'Manual control:CB OFF':
            bits = lookup_pointdict(self.thread_Serial.PCPoint.controlBits)
            bits |= 0x01
            update_pointdict(self.thread_Serial.PCPoint.controlBits, bits)
            bits_message = self.thread_Serial.PCPoint.writePointData(self.thread_Serial.PCPoint.controlBits, bits)
            self.thread_Serial.comPort.writeComPort(bits_message)
            self.pushButton_CBcontrol.setText("Manual control:CB ON")
        else:
            bits = lookup_pointdict(self.thread_Serial.PCPoint.controlBits)
            bits &= (~0x01)
            update_pointdict(self.thread_Serial.PCPoint.controlBits, bits)
            bits_message = self.thread_Serial.PCPoint.writePointData(self.thread_Serial.PCPoint.controlBits, bits)
            self.thread_Serial.comPort.writeComPort(bits_message)
            self.pushButton_CBcontrol.setText("Manual control:CB OFF")

##Debug
    def sendDebugAddr(self):
        string = self.textEdit_writeDebug.toPlainText()
        if string == " ":
            return
        addr = int(string, 16)
        if addr < 0 or addr > 0xFFFFFFFF:
            self.textBrowser_DebugReg.setText("Wrong Addr")
        addr1 = addr >> 16
        addr2 = addr & 0xFFFF
        message1 = self.thread_Serial.PCPoint.writePointData(self.thread_Serial.PCPoint.debug_addr1, addr1)
        message2 = self.thread_Serial.PCPoint.writePointData(self.thread_Serial.PCPoint.debug_addr2, addr2)
        self.thread_Serial.comPort.writeComPort(message1)
        self.thread_Serial.comPort.writeComPort(message2)


#plot
    def plotCurrentInit(self):
        self.graphicsView_current.setBackground('w')
        self.graphicsView_current.showGrid(x = True,y = True)
        self.graphicsView_current.enableAutoRange()
        mycurplot = self.graphicsView_current.plot([0],[0],pen = self.myPen)
        return mycurplot

    def plotVoltageInit(self):
        self.graphicsView_voltage.setBackground('w')
        self.graphicsView_voltage.showGrid(x=True, y=True)
        self.graphicsView_voltage.enableAutoRange()
        myvolplot = self.graphicsView_voltage.plot([0], [0],pen = self.myPen)
        return myvolplot

    def plotClear(self):
        self.thread_plot.t_vol = [0]
        self.thread_plot.t_cur = [0]
        self.thread_plot.voltage = [0]
        self.thread_plot.current = [0]

    def plotUpdate(self):
        try:
            self.mycurPlot.setData(self.thread_plot.t_cur, self.thread_plot.current)
            self.myvolPlot.setData(self.thread_plot.t_vol, self.thread_plot.voltage)
        except:
            self.textBrowser_batInfo.append("plot data wrong")

    def cellVoltageIndexUpdate(self):
        string = self.comboBox_plotcellchose.currentText()
        self.thread_plot.updateVoltageIndex(string)
        self.thread_plot.t_vol = [0]
        self.thread_plot.voltage = [0]


##############################################################
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.fuction = None



