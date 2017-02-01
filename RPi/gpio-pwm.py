import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
pwm = GPIO.PWM(4, 100) #ch12 freq50Hz
pwm.start(0)
try:
    while 1:
        for dc in range(0, 101, 5):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.5)
            print dc
        time.sleep(2)
        for dc in range (100, 0, -5):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.5)
            print dc
        time.sleep(2)
except KeyboardInterrupt:
    pass
pwm.stop()
GPIO.cleanup()
