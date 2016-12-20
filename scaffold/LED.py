import RPi.GPIO as GPIO
import time


def lightOn():
	print "LED on"
	GPIO.output(17,GPIO.HIGH)

def lightOff():
	print "LED off"
	GPIO.output(17,GPIO.LOW)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)

for i in range(0,10):
	lightOn()
	time.sleep(1)
	lightOff()
	time.sleep(1)
