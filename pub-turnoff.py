import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set fan pin 
FAN_PIN1 = 20

#set red,green and blue pins
redPin = 5
greenPin = 6
bluePin = 13

#set pins as outputs
GPIO.setup(FAN_PIN1, GPIO.OUT)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

def fanOff():
    #set as fan off
    GPIO.output(FAN_PIN1, True)

def lightOff():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)
    
fanOff()
lightOff()

