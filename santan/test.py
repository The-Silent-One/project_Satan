import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 26
GPIO_ECHO = 20

PLF=17
PLB=22
PRF=18
PRB=23
dt=0.5

GPIO.setup(PLF,GPIO.OUT)
GPIO.setup(PLB,GPIO.OUT)
GPIO.setup(PRF,GPIO.OUT)
GPIO.setup(PRB,GPIO.OUT)

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.output(PRF,0)
GPIO.output(PLF,0)
GPIO.output(PRB,0)
GPIO.output(PLB,0)


def forward(duration=0.5):
        GPIO.output(PLF,1)
        GPIO.output(PRF,1)
        GPIO.output(PLB,0)
        GPIO.output(PRB,0)
        time.sleep(duration)

def backward(duration=0.5):
        GPIO.output(PLB,1)
        GPIO.output(PRB,1)
        GPIO.output(PLF,0)
        GPIO.output(PRF,0)
        time.sleep(duration)

def left(duration=0.5):
	GPIO.output(PLF,1)
	GPIO.output(PRB,1)
	GPIO.output(PLB,0)
	GPIO.output(PRF,0)
	time.sleep(duration)

def right(duration=0.5):
        GPIO.output(PRF,1)
        GPIO.output(PLB,1)
        GPIO.output(PRB,0)
        GPIO.output(PLF,0)
        time.sleep(duration)


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
	    forward(0.1)
	    if dist<50:
		print("Stop")
		backward(0.5)
		GPIO.cleanup()
		break
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

