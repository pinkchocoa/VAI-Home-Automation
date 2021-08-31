import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set fan pin 
FAN_PIN2 = 16

#set red,green and blue pins
redPin = 13
greenPin = 19
bluePin = 26

#set pins as outputs
GPIO.setup(FAN_PIN2, GPIO.OUT)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

def fanOff():
    #set as fan off
    GPIO.output(FAN_PIN2,True)

def lightOff():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)
    
fanOff()
lightOff()

