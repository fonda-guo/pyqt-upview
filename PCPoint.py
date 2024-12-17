pointdict = {}
def update_pointdict(index,data):
    global pointdict
    pointdict[index] = data

def lookup_pointdict(index):
    global pointdict
    return pointdict[index]



class PCPoint:
    def __init__(self):
        self.cell1Vol = 0
        self.cell2Vol = 1
        self.cell3Vol = 2
        self.cell4Vol = 3
        self.cell5Vol = 4
        self.cell6Vol = 5
        self.cell7Vol = 6
        self.cell8Vol = 7
        self.cell9Vol = 8
        self.cell10Vol = 9
        self.cell11Vol = 10
        self.cell12Vol = 11
        self.cell13Vol = 12
        self.cell14Vol = 13
        self.cell15Vol = 14
        self.cell16Vol = 15
        self.stackVol = 16
        self.LDpinVol = 17
        self.alarmBits = 18
        self.safetyStatusA = 19
        self.safetyStatusB = 20
        self.safetyStatusC = 21
        self.fet_Status = 22
        self.ts1 = 23
        self.ts2 = 24
        self.ts3 = 25
        self.ts4 = 26
        self.current = 27
        self.test_cnter = 28
        #add here and change the number
        self.fault = 29
        self.u16_pc_buffer_num = 30

    def askPointData(self,index):
        str1 = "0700"
        str2 = "0000000A"
        pc_point_str = hex(index)[2:].rjust(4,'0')
        strp = str1 + pc_point_str + str2
        return bytes.fromhex(strp)
    def readPointData(self,rbytes):
        slave_addr = rbytes[0]
        rw = rbytes[1]
        pc_point = (rbytes[2] << 8) + rbytes[3]
        data = (rbytes[4] << 8)+rbytes[5]
        end = rbytes[7]
        if (slave_addr != 0x07) or (end != 0x0A):
            return -1, 0
        elif (rw != 0x11) and (rw != 0x12):
            return -1, 0
        elif rw == 0x11:
            if (pc_point >= self.u16_pc_buffer_num) or (pc_point < 0):
                return -1, 0
            else:
                update_pointdict(pc_point,data)
                return pc_point, data
        elif rw == 0x12:
            return -1, 0
            #to be done



