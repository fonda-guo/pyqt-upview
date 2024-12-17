import time

from PyQt5.QtCore import *
from comPort import COM
from PCPoint import *

class Thread_SerialHandle(QThread):
    data_received = pyqtSignal(bytes)
    showbatdata = pyqtSignal(int,int)
    data_lost = pyqtSignal()

    def __init__(self):
        super(Thread_SerialHandle, self).__init__()
        self.comPort = COM()
        self.PCPoint = PCPoint()
        self.pc_askindex = 0

    def run(self):
        while True:
            time.sleep(0.01)
            if self.comPort.openFlag:
                #keep asking mode
                # if self.pc_askindex == 0:
                #     t_start = time.perf_counter()
                if self.pc_askindex < self.PCPoint.u16_pc_buffer_num:
                  bytesmessage = self.PCPoint.askPointData(self.pc_askindex)
                  self.comPort.writeComPort(bytesmessage)
                  self.pc_askindex = self.pc_askindex + 1
                else:
                    self.pc_askindex = 0
                    continue
                # read
                data = self.comPort.readComPortEight()
                if data:
                    self.data_received.emit(data)
                    index,value = self.PCPoint.readPointData(data)
                    if index != -1:
                        self.showbatdata.emit(index,value)
                else:
                    self.data_lost.emit()
                # if self.pc_askindex == self.PCPoint.u16_pc_buffer_num:
                #     t_end = time.perf_counter()
                #     print(t_end - t_start)



