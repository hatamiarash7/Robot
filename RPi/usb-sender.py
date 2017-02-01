import serial
import time

t_end = time.time() + 120
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
ser.close()
ser.open()
print("write command")
while time.time() < t_end:
	Message = raw_input("Enter Message : ")
	ser.write(str(Message))
	ser.write('\r\n')
	time.sleep(0.1)
print("done")
