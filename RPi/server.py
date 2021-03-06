import os
from socket import *
import time
import numpy as np
import ctypes
import RPi.GPIO as GPIO
import re

HOST = ''
PORT = 80
Address = (HOST, PORT)
BUFFER = 1024
UDPSocket = socket(AF_INET, SOCK_DGRAM)
UDPSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
UDPSocket.bind(Address)
print "Start Bind ..."
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
print "setup GPIO ..."

GPIO.setup(4, GPIO.OUT)  # movement
GPIO.setup(3, GPIO.OUT)  # movement
GPIO.setup(27, GPIO.OUT) # movement
GPIO.setup(22, GPIO.OUT) # movement

GPIO.setup(17, GPIO.OUT) # arm up/down
GPIO.setup(18, GPIO.OUT) # arm left/right

GPIO.setup(10, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT) 

GPIO.setup(20, GPIO.OUT) # arenj
GPIO.setup(21, GPIO.OUT) # arenj

GPIO.setup(6, GPIO.OUT) # led

GPIO.setup(13, GPIO.OUT) 
GPIO.setup(10, GPIO.OUT)
 
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

GPIO.setup(8, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

GPIO.setup(7, GPIO.OUT)

print "start PWM ..."
pwm1 = GPIO.PWM(4, 200)
pwm2 = GPIO.PWM(3, 200)
pwm3 = GPIO.PWM(27, 200)
pwm4 = GPIO.PWM(22, 200)
pwm5 = GPIO.PWM(17, 100) 
pwm6 = GPIO.PWM(18, 200) 
pwm7 = GPIO.PWM(19, 500) 
pwm8 = GPIO.PWM(26, 500)
pwm9 = GPIO.PWM(20, 500)
pwm10 = GPIO.PWM(21, 500) 
pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)
pwm5.start(0)
pwm6.start(0)
pwm7.start(0)
pwm8.start(0)
pwm9.start(0)
pwm10.start(0)
print "let's go ..."
stop = True
arm = True
GPIO.output(10, True)
GPIO.output(13, True)
GPIO.output(9, True)
GPIO.output(11, True)
GPIO.output(8, True)
GPIO.output(25, True)
GPIO.output(6, True)
pwm7.ChangeDutyCycle(0)
pwm8.ChangeDutyCycle(0)
pwm9.ChangeDutyCycle(0)
pwm10.ChangeDutyCycle(0)

while True:
    (Message, Address) = UDPSocket.recvfrom(BUFFER)
    #print "Message : " + Message
    if Message == "exit":
        break
    indata = re.findall(r"[\w']+", Message)
    if len(indata)==2:
        cmd = str(indata[0])
        spd = float(indata[1])
        if spd <= 25:
            f=spd
            b=56-spd
        elif spd >= 31:
            f=56-spd
            b=spd
        if cmd == "Forward":
            pwm1.ChangeDutyCycle(f)
            pwm2.ChangeDutyCycle(f)
            pwm3.ChangeDutyCycle(f)
            pwm4.ChangeDutyCycle(f)
            time.sleep(0.1)
            stop=True
        elif cmd == "Backward":
            pwm1.ChangeDutyCycle(b)
            pwm2.ChangeDutyCycle(b)
            pwm3.ChangeDutyCycle(b)
            pwm4.ChangeDutyCycle(b)
            time.sleep(0.1)
            stop=True
        elif cmd == "Left":
            pwm1.ChangeDutyCycle(b)
            pwm2.ChangeDutyCycle(b)
            pwm3.ChangeDutyCycle(f)
            pwm4.ChangeDutyCycle(f)
            time.sleep(0.1)
            stop=True
        elif cmd == "Right":
            pwm1.ChangeDutyCycle(f)
            pwm2.ChangeDutyCycle(f)
            pwm3.ChangeDutyCycle(b)
            pwm4.ChangeDutyCycle(b)
            time.sleep(0.1)
            stop=True
        elif cmd == "ArmUP":
            pwm5.ChangeDutyCycle(8)
            time.sleep(0.12)
            stop = True
        elif cmd == "ArmDown":
            pwm5.ChangeDutyCycle(23)
            time.sleep(0.12)
            stop = True
        elif cmd == "ArmLeft":
            pwm6.ChangeDutyCycle(40)
            time.sleep(0.12)
            stop=True
        elif cmd == "ArmRight":
            pwm6.ChangeDutyCycle(10)
            time.sleep(0.12)
            stop=True
        elif cmd == "ArenjUP":
            GPIO.output(19, False)
            pwm9.ChangeDutyCycle(99)
            time.sleep(0.11)
            stop=True
        elif cmd == "ArenjDown":
            GPIO.output(26, False)
            pwm10.ChangeDutyCycle(99)
            time.sleep(0.11)
            stop=True
        elif cmd == "GripperOpen":
            GPIO.output(19, False)
            pwm7.ChangeDutyCycle(99)
            time.sleep(0.1)
            stop=True
        elif cmd == "GripperClose":
            GPIO.output(26, False)
            pwm8.ChangeDutyCycle(99)
            time.sleep(0.1)
            stop = True
        elif cmd == "R1":
            GPIO.output(11, True)
            GPIO.output(9, False)
            stop = True
        elif cmd == "R2":
            GPIO.output(11, False)
            GPIO.output(9, True)
            stop = True
        elif cmd == "R3":
            GPIO.output(8, True)
            GPIO.output(25, False)
            stop = True
        elif cmd == "R4":
            GPIO.output(8, False)
            GPIO.output(25, True)
            stop = True
        elif cmd == "ArmOff" and not arm:
            GPIO.output(8, True)
            GPIO.output(11, True)
        elif cmd == "Stop" and stop:
            pwm1.ChangeDutyCycle(28)
            pwm2.ChangeDutyCycle(28)
            pwm3.ChangeDutyCycle(28)
            pwm4.ChangeDutyCycle(28)
            pwm5.ChangeDutyCycle(14)
            pwm6.ChangeDutyCycle(28)
            time.sleep(0.01)
            pwm1.ChangeDutyCycle(0)
            pwm2.ChangeDutyCycle(0)
            pwm3.ChangeDutyCycle(0)
            pwm4.ChangeDutyCycle(0)
            pwm5.ChangeDutyCycle(0)
            pwm6.ChangeDutyCycle(0)
            pwm7.ChangeDutyCycle(0)
            pwm8.ChangeDutyCycle(0)
            pwm9.ChangeDutyCycle(0)
            pwm10.ChangeDutyCycle(0)
            GPIO.output(19, False)
            GPIO.output(26, False)
            GPIO.output(20, False)
            GPIO.output(21, False)
            GPIO.output(7, True)
            GPIO.output(8, True)
            GPIO.output(9, True)
            GPIO.output(25, True)
            GPIO.output(11, True)
            GPIO.output(13, True)
            GPIO.output(10, True)
            GPIO.output(6, True)
            stop = False
UDPSocket.close()
pwm1.stop()
pwm2.stop()
pwm3.stop()
pwm4.stop()
GPIO.cleanup()
os._exit(0)
