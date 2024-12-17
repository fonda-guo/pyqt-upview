# import pyvisa
#
# rm = pyvisa.ResourceManager()
# rm_address = rm.list_resources('?*')
# print(rm_address, type(rm_address))
# try:
#     my_instrument = rm.open_resource('rm_address[0]')
#     # my_instrument.write_termination = '\n'
#     my_instrument.read_termination = '\n'
#
# except:
#     print(my_instrument.query('*IDN?\n'))
#     print('Wrong device name & type')
import time

# b = "070000060000000A"
# d = bytes.fromhex(b)
# e = d.hex()
# res = d[0]
# print(type(e))
#
# addr = (b.encode('utf8').hex()=='0A')
# c = "1".encode('utf8').hex()
# d = int(c,16)

# index = 5
# f = hex(index)[2:]
# ans = f.rjust(4,'0')
# print(ans)

# str1 = "asd"
# str2 = str1+str(1);
# print(str2)

t1 = time.perf_counter()
time.sleep(0.001)
t2 = time.perf_counter()
print(t2-t1)