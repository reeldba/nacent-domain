# nacent-domain -- Quill-I-Am's automated habitat

## Purpose

So my family keeps and raises pygmy hedgehogs.  
Hedgies are warm weather critters and do best when their habitat is kept 
around 74-78 degrees farenheit.   If it goes any lower than 72 the little 
guys can start to go into a hibernation state that they are not really 
capable of and this can lead to all kinds of bad things including your 
beloved little pin-cushion dying.

So this project seeks to automate the temperature of the habitat by measuring
the temperature and then remotely turning on a heat lamp and / or a hot-spot
warming spot fo the hedgie.

If successful, this should (a) keep hedgie warm and happy year round, (b) pay
for itself pretty quickly in reduced utility bills and (c) make my wife and
daughter very happy.

## Parts List

* Raspberry Pi 3 Model B.  This is overkill - but overkill is under-rated.  I
may enable the remote receptacles to wake up my teenager on weekdays.
* Adafruit DHT-8302 Temperature and Humidity Sensor
* SMAKN 433Mhz Receiver and Transmitter
* Elektracity 5 Pack remote controlled outlets

Note - I bought the Adafruit starter pack for this project.  Those guys rock.
It arrived in no time.

## Software

I'm using these libraries, plus what I write

* Adaafruit DHT Libraries
