import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PLF=17
PLB=22
PRF=18
PRB=23
dt=0.5
wait_time=5
GPIO.setup(PLF,GPIO.OUT)
GPIO.setup(PLB,GPIO.OUT)
GPIO.setup(PRF,GPIO.OUT)
GPIO.setup(PRB,GPIO.OUT)

GPIO.output(PRF,0)
GPIO.output(PLF,0)
GPIO.output(PRB,0)
GPIO.output(PLB,0)

time.sleep(1)

def stop(d):
    GPIO.output(PLF,0)
    GPIO.output(PRF,0)
    GPIO.output(PLB,0)
    GPIO.output(PRB,0)
    time.sleep(d)
    
def forward(duration=0.5):
    GPIO.output(PLF,1)
    GPIO.output(PRF,1)
    GPIO.output(PLB,0)
    GPIO.output(PRB,0)
    time.sleep(duration)
    stop(1)

def backward(duration=0.5):
    GPIO.output(PLB,1)
    GPIO.output(PRB,1)
    GPIO.output(PLF,0)
    GPIO.output(PRF,0)
    time.sleep(duration)
    stop(1)

def left(duration=0.5):
    GPIO.output(PLF,1)
    GPIO.output(PRB,1)
    GPIO.output(PLB,0)
    GPIO.output(PRF,0)
    time.sleep(duration)
    stop(1)

def right(duration=0.5):
    GPIO.output(PRF,1)
    GPIO.output(PLB,1)
    GPIO.output(PRB,0)
    GPIO.output(PLF,0)
    time.sleep(duration)
    stop(1)

def move(t):
    for i in range(len(t)):
        if(i!=0 and t[i]==t[i-1]):
            forward(dt)
        else:
            if(t[i]=="L"):
                left(dt)
                forward(dt)
            elif(t[i]=="R"):
                right(dt)
                forward(dt)
            elif(t[i]=="U"):
                forward(dt)
            elif(t[i]=="D"):
                backward(dt)
    time.sleep(wait_time)
    right(dt)
    right(dt)
    for i in range(len(t)-1,1,-1):
        if(i!=len(t)-1 and t[i]!=t[i+1]):
            if(t[i]=="U" and t[i+1]!=t[i]):
                if(t[i]=="U" and t[i+1]=='L'):
                    right(dt)
                    forward(dt)
                elif(t[i]=="U" and t[i+1]=="R"):
                    left(dt)
                    forward(dt)
                elif(t[i]=="D" and t[i+1]=="L"):
                    left(dt)
                    forward(dt)
                elif(t[i]=="D" and t[i+1]=="R"):
                    right(dt)
                    forward(dt)
        else:
            forward(dt)
                
move(['U','R'])

GPIO.cleanup()
