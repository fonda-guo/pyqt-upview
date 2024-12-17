import pyvisa

class SCPI:
    def __init__(self):
        self.rm = None
        self.portName = ''
        self.actionPower = None
        self.openFlag = False

    def openSCPI(self):
        self.rm = pyvisa.ResourceManager()
        rm_address = self.rm.list_resources('?*')
        if len(rm_address) == 0:
            return "No device detected"
        else:
            self.portName = rm_address[0]
            try:
                self.actionPower = self.rm.open_resource(self.portName)
                self.actionPower.write_termination = '\n'
                self.actionPower.read_termination = '\n'
                self.openFlag = True
                return self.portName+" detected and opened successfully"
            except:
                return "Wrong device name & type"

    def writeSCPI(self, writeStr):
        if self.openFlag:
            self.actionPower.write(writeStr)

    def querySCPI(self, queryStr):
        if self.openFlag:
            return self.actionPower.query(queryStr,delay = 0.01)
