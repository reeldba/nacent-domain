#!/usr/bin/env python
# -----------------------------------------------------------------------------
# File: habitat.py
# Created: 2016 Dec 20 19:34:04
# Author: reeldba@gmail.com
# -----------------------------------------------------------------------------
# Purpose:      This program controls the habitat for a small mammal, in this
#               case a hedgehog, within some parameters for temperature.
# Description:
# Synopsis:
# Exit Status:
# -----------------------------------------------------------------------------

import gpiozero
import RPi.GPIO as GPIO
import datetime
import Adafruit_DHT
import logging
import time

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

# -----------------------------------------------------------------------------
# Set Logging up First
# -----------------------------------------------------------------------------
from logging.handlers import RotatingFileHandler
datalogger = logging.getLogger()
datalogger.setLevel(logging.INFO)
datahandler=logging.handlers.RotatingFileHandler('habitat.log',maxBytes=256*1024,backupCount=5)
formatter=logging.Formatter("%(asctime)s %(message)s","%Y-%m-%d %H:%M:%S")
datahandler.setFormatter(formatter)
datalogger.addHandler(datahandler)


# -----------------------------------------------------------------------------
# Heater Control 
# -----------------------------------------------------------------------------
def HeaterControl(toggle):
	if toggle == 1 :
		print "heater on"
	elif toggle == 0 :
		print "heater off"

# -----------------------------------------------------------------------------
# record_observations -- store the observations somewhere for safe keeping.
# -----------------------------------------------------------------------------
def record_observation(field1,field2,field3):

	# record this to a local file and then to thingspeak
	print('{0} Temp={1:0.1f}*C Humidity={2:0.1f}% {3}'\
		.format(datetime.datetime.utcnow(),field1,field2,field3))

	#datalogger.info("{0:0.1f},{1:0.1f},{2}".format(field1,field2,field3))
	datalogger.info("{0:0.1f},{1:0.1f}".format(field1,field2))

	# TODO - need something to detect when we haven't seen a reading and then
    #        alarm - doesn't belong in this file - but we need it


# -----------------------------------------------------------------------------
# MAIN LINE OF CODE STARTS HERE
# -----------------------------------------------------------------------------

# Step 1 - record the temperature and humidity
humidity,temperature = Adafruit_DHT.read_retry(SENSOR,SENSOR_PIN)

if humidity is None or temperature is None:
	# couldn't get a reading on one or both of the measures
	record_observation(field1=temperature,\
		field2=humidity, \
		field3="failed to get a reading")

else:
	record_observation(field1=temperature, field2=humidity, field3="got a reading")
	if temperature < TARGET_TEMPERATURE:
		if temperature < LOWER_CONTROL_LIMIT:
			rc=HeaterControl(1)
			if temperature < LOWER_ALERT_LIMIT:
				# alert someone
				print "<<"
		else:
			print "<"


	elif temperature > TARGET_TEMPERATURE:
		if temperature > UPPER_CONTROL_LIMIT:
			rc=HeaterControl(0)
			if temperature > UPPER_CONTROL_LIMIT:
				# alert someone
				print ">"
	else:
		# must have equaled it
		print "="

# ===========================================================================
# clean up
# ===========================================================================

# ===========================================================================
#
# ===========================================================================

# vim: ts=4 number
