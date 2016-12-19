#!/usr/bin/python
import gpiozero
import RPi.GPIO as GPIO
import datetime
import Adafruit_DHT

# NOTE - REPLACE THIS WITH A CONFIG JSON 
SENSOR=Adafruit_DHT.AM2302
SENSOR_PIN=23

TARGET_TEMPERATURE=26.67
LOWER_CONTROL_LIMIT=23.88
UPPER_CONTROL_LIMIT=29.44
LOWER_ALERT_LIMIT=19.00
UPPER_ALERT_LIMIT=31.00


# PUT A LOCK IN PLACE - DON'T LET A SECOND INSTANCE FIRE UP IF WE ARE 
# STILL WAITING ON THIS INSTANCE TO FINISH
#
# lock me here
#


def record_observation(field1,field2,field3):
	print('{0} Temp={1:0.1f}*C Humidity={2:0.1f}% {3}'.format(datetime.datetime.utcnow(),field1,field2,field3))

# ===========================================================================
# MAIN LINE OF CODE STARTS HERE
# ===========================================================================

# Read the sensors
humidity,temperature = Adafruit_DHT.read_retry(SENSOR,SENSOR_PIN)

if humidity is none or temperature is none:
	# couldn't get a reading
	record_observation(field1=temperature, field2=humidity, field3="failed to get a reading")


else;

	if temperature < TARGET_TEMPERATURE:
		if temperature < LOWER_CONTROL_LIMIT:
			rc=RemoteHeater(on)
			if temperature < LOWER_ALERT_LIMIT:
				# alert someone
		else:


	elif temperature > TARGET_TEMPERATURE:
		if temperature > UPPER_CONTROL_LIMIT:
			rc=remoteHeater(off)
			if temperature > UPPER_CONTROL_LIMIT:
				# alert someone
	else:
		# must have equaled it

# ===========================================================================
# clean up
# ===========================================================================

# vim: ts=4 number
