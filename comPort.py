import serial
import serial.tools.list_ports

class COM:
    def __init__(self):
        self.port = 0
        self.baud = 115200
        self.open_com = None
        self.ser = None
        self.openFlag = 0
        self.data = ''
        self.isSendLock = False

    def list_port(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            return ("None")
        else:
            return (port_list)

    def openComPort(self,comName,baudRate):
        self.ser = serial.Serial(comName, baudRate, timeout=0.01)
        self.openFlag = self.ser.is_open
        return self.openFlag

    def closeComPort(self):
        self.ser.close()
        self.openFlag = self.ser.is_open

    def writeComPort(self,message):
        if self.openFlag and (not self.isSendLock):
            self.isSendLock = True
            writeNum = self.ser.write(message)
            self.isSendLock = False
            return writeNum
        else:
            return 0


    def readComPortEight(self):
        if self.openFlag: #and (self.ser.inWaiting() >0):
            data = self.ser.read(8)
            return data
        else:
            return False