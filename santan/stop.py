import RPI.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

PLF=17
PLB=22
PRF=18
PRB=23
duration=0.5

GPIO.setup(PLF,GPIO.OUT)
GPIO.setup(PLB,GPIO.OUT)
GPIO.setup(PRF,GPIO.OUT)
GPIO.setup(PRB,GPIO.OUT)


GPIO.cleanup()
