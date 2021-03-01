import paho.mqtt.client as mqtt

#Fan
import time
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LED_PIN2 = 23
GPIO.setup(LED_PIN2, GPIO.OUT)

FAN_PIN2 = 19
GPIO.setup(FAN_PIN2, GPIO.OUT)
 
PUSH_BTN = 4
GPIO.setup(PUSH_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

MQTTBROKER = 'iot.eclipse.org'
PORT = 1883

TOPIC = "home/fan"
MESSAGE = "FanOn"

mqttc = mqtt.Client("python_pub")
mqttc.connect(MQTTBROKER, PORT)
mqttc.publish(TOPIC, MESSAGE)

buttonPress = True
ledState = False

while True:
    buttonPress = GPIO.input(PUSH_BTN)
    if buttonPress == False and ledState == False:
        GPIO.output(LED_PIN2, True)
        GPIO.output(FAN_PIN2, True)
        ledState = True
       
        MESSAGE = "ON"
        mqttc.publish(TOPIC, MESSAGE)
        print("Published to " + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)
        
    elif buttonPress == False and ledState == True:
        GPIO.output(LED_PIN2, False)
        GPIO.output(FAN_PIN2, False)
        ledState = False
        
        MESSAGE = "Off"
        mqttc.publish(TOPIC, MESSAGE)
        print("Published to " + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)
    
mqttc.loop(2)
        
    
