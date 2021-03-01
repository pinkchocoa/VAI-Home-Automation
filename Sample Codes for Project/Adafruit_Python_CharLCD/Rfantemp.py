#!/usr/bin/python3
import time
import os
import sys
import RPi.GPIO as GPIO

# Identify which pin controls the relay
FAN_PIN = 24
# Temperature check. Start fan after 50C, Shut down under 50C
FAN_START = 50

def GPIOsetup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT)
    GPIO.setwarnings(False)

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def fanON():
    GPIO.output(FAN_PIN, 0)
    print ("fan on")
    return()

def fanOFF():
    GPIO.output(FAN_PIN, 1)
    print ("fan off")
    return()

def getTEMP():
    CPU_temp = float(getCPUtemperature())
    if CPU_temp>FAN_START:
        fanON()
    else:
        fanOFF()
    return()

def main():
    GPIOsetup()
    getTEMP()

try:
    main()
finally:
    print ("Finish")
    #GPIO.cleanup()