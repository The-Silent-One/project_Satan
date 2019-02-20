import RdPi.GPIO as GPIO
import time
from gpiozero import Motor
from gpiozero import DistanceSensor

GPIO.setmode(GPIO.BCM)
pwmD=13 #pin33
pwmG=19 #pin35

motorD = Motor(17, 18) #pin11,12
motorG = Motor(22, 27) #pin13,15
aspirateur = Motor(23, 24) #pin16,18

ECHO = 5 #PIN29
TRIG = 6 #PIN31

GPIO.setup(pwmD,GPIO.OUT)
GPIO.setup(pwmG,GPIO.OUT)

pD=GPIO.PWM(pwmD,100)
pD.start(25)

pG=GPIO.PWM(pwmG,100)
pG.start(25)

def forward():
    motorD.forward()
    motorG.forward()
    print('forward')

def back():
    motorD.backward()
    motorG.backward()
    print('backward')
    
def left():
    motorD.stop()
    motorG.forward()
    print('left')
    
def right():
    motorD.forward()
    motorG.stop()
    print('right')
    
def stop():
    motorD.stop()
    motorG.stop()
    print('stop')

def aspirateurON():
    aspirateur.forward()
    print('AspirateurON')
    
def aspirateurOFF():
    aspirateur.stop()
    print('AspirateurOFF')
stop()
count=0
while True:
 i=0
 avgDistance=0
 for i in range(5):
  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  time.sleep(0.1)                                   #Delay

  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
  time.sleep(0.00001)                           #Delay of 0.00001 seconds
  GPIO.output(TRIG, False)                 #Set TRIG as LOW

  while GPIO.input(ECHO)==0:              #Check whether the ECHO is LOW
                    
  pulse_start = time.time()

  while GPIO.input(ECHO)==1:              #Check whether the ECHO is HIGH
       
  pulse_end = time.time()
  pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor

  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
  distance = round(distance,2)                 #Round to two decimal points
  avgDistance=avgDistance+distance

 avgDistance=avgDistance/5
 print avgDistance
 flag=0
 if avgDistance < 25 :      #Check whether the distance is within 15 cm range
    count=count+1
    stop()
    time.sleep(1)
    back()
    time.sleep(1.5)
    if (count%3 ==1) & (flag==0):
     right()
     flag=1
    else:
     left()
     flag=0
    time.sleep(1.5)
    stop()
    time.sleep(1)
 else:
    forward()
    flag=0

