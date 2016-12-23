#!/usr/bin/env python
# -------------------------------------------------------------------------
# File: habitat.py
# Created: 2016 Dec 20 19:34:04
# Author: reeldba@gmail.com
# -------------------------------------------------------------------------
# Purpose:    This program controls the habitat for a small mammal, in 
#             this case a hedgehog, within some parameters for temperature.
# Description:
# Synopsis:
# Exit Status:
# -------------------------------------------------------------------------

import sys
import os
import stat
import fcntl
import gpiozero
import RPi.GPIO as GPIO
import datetime
import Adafruit_DHT
import logging
import time
import json

# ------------------------------------------------------------------------
# Instance Lock - don't allow more than one instance of this code to run
# ------------------------------------------------------------------------
lf_path='/tmp/habitat.lock'
lf_flags=os.O_WRONLY|os.O_CREAT
lf_mode=stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
umask_original=os.umask(0)
try:
	lf_fd=os.open(lf_path,lf_flags,lf_mode)
except IOError as er:
	print('IO Error:{0} attempting to open lock file'.format(er.strerror))
finally:
	os.umask(umask_original)

try:
	fcntl.lockf(lf_fd,fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError as er:
	print('IO Error:{0} attempting to lock file'.format(er.strerror))

# ------------------------------------------------------------------------
# Read the Config File
# -------------------------------------------------------------------------
try:
	with open("habitat.json",'r') as json_data_file:
		config=json.load(json_data_file)
except IOError:
	print("Cannot find habitat.json or read data from it.")
	exit(1)

# NOTE - REPLACE THIS WITH A CONFIG JSON 
SENSOR=Adafruit_DHT.AM2302
SENSOR_PIN=23

TARGET_TEMPERATURE=26.67
LOWER_CONTROL_LIMIT=23.88
UPPER_CONTROL_LIMIT=29.44
LOWER_ALERT_LIMIT=19.00
UPPER_ALERT_LIMIT=31.00

# -------------------------------------------------------------------------
# Set Logging up First.   This will be a simple data logger using the 
# rotating log file handler.  As it is set up, no more than 5 x 256K bytes 
# worth of data will be kept
# -------------------------------------------------------------------------
from logging.handlers import RotatingFileHandler
datalogger = logging.getLogger()
datalogger.setLevel(logging.INFO)
datahandler=logging.handlers.RotatingFileHandler('habitat.log',maxBytes=256*1024,backupCount=5)
formatter=logging.Formatter("%(asctime)s %(message)s","%Y-%m-%d %H:%M:%S")
datahandler.setFormatter(formatter)
datalogger.addHandler(datahandler)


# -------------------------------------------------------------------------
# Heater Control.This is a stub for the code that will transmit RF signals
# to the remote heater unit 
# -------------------------------------------------------------------------
def HeaterControl(toggle):
	# step 1 get the current state of the file
	ts=datetime.datetime.utcnow()	
	try:
		with open("habitat.heater_state","r") as heaterStateFile:
			heater_state=heaterStateFile.readlines()
			heaterStateFile.close()
	except IOError as er:
		sys.stderr.write("err msg fix me\n")

	if toggle == 1:
		if heater_state[0] == 'ON':
			print "Heater Remains On"
			heater_state="ON"
		else:
			print "Turning Heater On."
			heater_state="ON"
	elif toggle == 0:
		if heater_state[0] == 'ON':
			print "Turning Heater Off."
			heater_state="OFF"
		else:
			print "Heater Remains Off"
			heater_state="OFF"
	try:
		with open("habitat.heater_state","w") as heaterStateFile:
			heater_state=heaterStateFile.write(heater_state)
			heaterStateFile.close()
	except IOError as er:
		sys.stderr.write("err msg 2 fix me\n")

# -------------------------------------------------------------------------
# record_observations -- store the observations somewhere for safe keeping.
# -------------------------------------------------------------------------
def record_observation(field1,field2,field3):
	import requests

	ts=datetime.datetime.utcnow()

	# first thing, lets write the data to the local disk
	try:
		with open("habitat.dat","a") as datafile:
			datafile.write("{0},{1:0.1f},{2:0.1f},{3:s}\n".format(ts,field1,field2,field3))
	except IOError as er:
		sys.stderr.write("Error writing data {0}".format(er.strerror))

	try:
		r = requests.post(config['cfg']['thingspeak_update_url'],data={'api_key':config['cfg']['thingspeak_write_key'],'field1':field1,'field2':field2}) 
	except Exception as er:
		sys.stderr.write("Error posting to thingspeak {0}".format(er.strerror))


# -------------------------------------------------------------------------
# MAIN LINE OF CODE STARTS HERE
# -------------------------------------------------------------------------

# Step 1 - record the temperature and humidity
humidity,temperature = Adafruit_DHT.read_retry(SENSOR,SENSOR_PIN)

if humidity is None or temperature is None:
	# couldn't get a reading on one or both of the measures
	record_observation(field1=temperature,\
		field2=humidity, \
		field3="failed to get a reading")

else:
	record_observation(field1=temperature, field2=humidity, field3="OK")
	if temperature < TARGET_TEMPERATURE:
		if temperature < LOWER_CONTROL_LIMIT:
			print "temperature lower than lower control limit"
			rc=HeaterControl(1)
			if temperature < LOWER_ALERT_LIMIT:
				# alert someone
				print "temperature lower than lower alert limit"
				rc=HeaterControl(1)
		else:
			print "temp lower than target but higher than lower control"
			rc=HeaterControl(1)


	elif temperature > TARGET_TEMPERATURE:
		if temperature > UPPER_CONTROL_LIMIT:
			rc=HeaterControl(0)
			if temperature > UPPER_CONTROL_LIMIT:
				# alert someone
				print ">"
	else:
		# must have equaled it
		print "="

# =========================================================================
# clean up
# =========================================================================

# =========================================================================
#
# =========================================================================

# vim: set number on:ts=4
