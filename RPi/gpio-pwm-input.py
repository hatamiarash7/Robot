import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
pwm = GPIO.PWM(4, 100) #ch12 freq50Hz
pwm.start(0)
try:
    while 1:
        dc = raw_input("Enter Value : ")
        dc = float(dc)
        pwm.ChangeDutyCycle(dc)
except KeyboardInterrupt:
    pass
pwm.stop()
GPIO.cleanup()
