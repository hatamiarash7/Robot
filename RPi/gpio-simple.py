import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
try:
    while 1:
        GPIO.output(16, 1)
        time.sleep(0.5)
        GPIO.output(16, 0)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
GPIO.cleanup()