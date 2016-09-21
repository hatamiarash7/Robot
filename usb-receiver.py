import serial
import re

def cleanup(x, notwanted):
    for item in notwanted:
        x = re.sub(item, '', x)
    return x

com = serial.Serial('/dev/ttyUSB0')
com.baudrate = 9600
com.bytesize = 8
com.parity = 'N'
com.stopbits = 1
com.close()
com.open()
while True:
    data = com.readline()
    data = str(data)
    #data = re.sub("['b\\/n]", '', data)
    #remove = ["n\\'n/"]
    #data = cleanup(data, remove)
    #data = data.replace("\\", "")
    if data == "exit" or data == "Exit":
        print "Exiting ..."
        break
    else:
        print(data)
com.close()
