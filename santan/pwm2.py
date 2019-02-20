import RPi.GPIO as GPIO
import time
from gpiozero import Motor

GPIO.setmode(GPIO.BCM)

PLF=17
PLB=22
PRF=18
PRB=23


pwmD=2 #pin33
pwmG=3 #pin35

#motorD = Motor(17, 18) #pin11,12
#motorG = Motor(22, 23) #pin13,15

motorD = Motor(PRF, PRB) #pin11,12
motorG = Motor(PLF, PLB) #pin13,15

GPIO.setup(pwmD,GPIO.OUT)
GPIO.setup(pwmG,GPIO.OUT)

pD=GPIO.PWM(pwmD,100)
pD.start(25)

pG=GPIO.PWM(pwmG,100)
pG.start(25)

motorD.forward(1)
motorD.ChangeDutyCycle(12.5)
#motorG.forward()
time.sleep(3)

#GPIO.cleanup()
