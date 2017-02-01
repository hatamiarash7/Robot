import serial
import time
import re
import threading
from threading import Thread


ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=9600,
	bytesize=serial.EIGHTBITS,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	xonxoff=serial.XOFF,
	rtscts=False,
	dsrdtr=False
	)

com = serial.Serial('/dev/ttyUSB0')
com.baudrate = 9600
com.bytesize = 8
com.parity = 'N'
com.stopbits = 1

ser.close()
ser.open()




def cleanup(x, notwanted):
    for item in notwanted:
        x = re.sub(item, '', x)
    return x


def receive():
    data = ser.readline()
    data = str(data)
    data = re.sub("['b\\/n]", '', data)
    remove = ["n\\'n/"]
    data = cleanup(data, remove)
    data = data.replace("\\", "")
    print ("Other Said : " + data)

def send():
    Message = raw_input("You Said : ")
    ser.write(str(Message))
    ser.write('\r\n')
    time.sleep(0.1)

print("Welcome To Chat App")
while True:
    Thread(target = receive).start()
    Thread(target = send).start()
print("Goodby :)")
