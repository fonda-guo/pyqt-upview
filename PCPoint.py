pointdict = {}
def update_pointdict(index,data):
    global pointdict
    if (index >= 0) and (index <= PCPoint.LDpinVol):
        pointdict[index] = format(data / 1000, '.3f')
    elif (index >= PCPoint.ts1) and (index <= PCPoint.ts4):
        pointdict[index] = format(data/10, '.1f')
    elif index == PCPoint.current:
        if data > 32767:
            data = data - 65536
        pointdict[index] = format(data / 25, '.1f')
    elif PCPoint.SOC_box <= index <= PCPoint.SOH_box:
        pointdict[index] = format(data / 100, '.2f')
    elif PCPoint.maxcellvol <= index <= PCPoint.mincellvol:
        pointdict[index] = format(data / 1000, '.3f')

def lookup_pointdict(index):
    global pointdict
    if index in pointdict:
        return pointdict[index]
    else:
        return 0xffff



class PCPoint:
    cell1Vol = 0
    cell2Vol = 1
    cell3Vol = 2
    cell4Vol = 3
    cell5Vol = 4
    cell6Vol = 5
    cell7Vol = 6
    cell8Vol = 7
    stackVol = 8
    LDpinVol = 9
    alarmBits = 10
    safetyStatusA = 11
    safetyStatusB = 12
    safetyStatusC = 13
    fet_Status = 14
    ts1 = 15
    ts2 = 16
    ts3 = 17
    ts4 = 18
    current = 19
    test_cnter = 20
    debug_register1 = 21
    debug_register2 = 22
    SOC_box = 23
    SOC_cell1 = 24
    SOC_cell2 = 25
    SOC_cell3 = 26
    SOC_cell4 = 27
    SOC_cell5 = 28
    SOC_cell6 = 29
    SOC_cell7 = 30
    SOC_cell8 = 31
    SOH_box = 32
    maxcellvol = 33
    mincellvol = 34
    # add here and change the number
    fault = 35
    # here is to wirte
    debug_addr1 = 36
    debug_addr2 = 37
    u16_pc_buffer_num = 38
    def __init__(self):
        a = 1+1
        # self.cell1Vol = 0
        # self.cell2Vol = 1
        # self.cell3Vol = 2
        # self.cell4Vol = 3
        # self.cell5Vol = 4
        # self.cell6Vol = 5
        # self.cell7Vol = 6
        # self.cell8Vol = 7
        # self.stackVol = 8
        # self.LDpinVol = 9
        # self.alarmBits = 10
        # self.safetyStatusA = 11
        # self.safetyStatusB = 12
        # self.safetyStatusC = 13
        # self.fet_Status = 14
        # self.ts1 = 15
        # self.ts2 = 16
        # self.ts3 = 17
        # self.ts4 = 18
        # self.current = 19
        # self.test_cnter = 20
        # #add here and change the number
        # self.fault = 21
        # self.u16_pc_buffer_num = 22

    def askPointData(self,index):
        str1 = "0700"
        str2 = "0000000A"
        pc_point_str = hex(index)[2:].rjust(4,'0')
        strp = str1 + pc_point_str + str2
        return bytes.fromhex(strp)

    def writePointData(self,index,data):
        str1 = "0701"
        str2 = "000A"
        pc_point_str  = hex(index)[2:].rjust(4, '0')
        pc_point_data = hex(data)[2:].rjust(4, '0')
        strp = str1 + pc_point_str + pc_point_data + str2
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



