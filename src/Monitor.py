import RPi.GPIO as GPIO
import datetime
import Adafruit_DHT

SENSOR=Adafruit_DHT.AM2302
SENSOR_PIN=23

humidity,temperature = Adafruit_DHT.read_retry(SENSOR,SENSOR_PIN)

if humidity is not None and temperature is not None:
	print('{0} Temp={1:0.1f}*C Humidity={2:0.1f}%'.format(datetime.datetime.utcnow(),temperature,humidity))
else:
	print('{0} Temp=None Humidity=None'.format(datetime.datetime.utcnow()))

# vim: ts=4 number
