import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#set red,green and blue pins
redPin = 5
greenPin = 6
bluePin = 13
#set pins as outputs
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

def turnOff():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)
    
def white():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.LOW)

PUSH_BTN = 18
GPIO.setup(PUSH_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
MQTTBROKER = 'test.mosquitto.org'
PORT = 1883
TOPIC = 'home/light'
MESSAGE = 'ON'
mqttc = mqtt.Client('python_pub')
mqttc.connect(MQTTBROKER, PORT)
mqttc.publish(TOPIC, MESSAGE)

buttonPress = True
ledState = False

while True:
    buttonPress = GPIO.input(PUSH_BTN)
    
    if buttonPress == False and ledState == False:
        
        white()
  
        ledState = True
        
        MESSAGE = 'On'
        mqttc.publish(TOPIC, MESSAGE)
        
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)
        
    elif buttonPress == False and ledState == True:
        turnOff()
  
        ledState = False
        
        MESSAGE = 'Off'
        mqttc.publish(TOPIC,MESSAGE)
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)

        
mqttc.loop(2)
