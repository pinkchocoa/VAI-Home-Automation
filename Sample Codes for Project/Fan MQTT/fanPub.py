import paho.mqtt.client as mqtt

#Fan
import time
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PUSH_BTN = 26
GPIO.setup(PUSH_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

MQTTBROKER = 'iot.eclipse.org'
PORT = 1883

TOPIC = "home/doorbell"
MESSAGE = "FanOn"

mqttc = mqtt.Client("python_pub")
mqttc.connect(MQTTBROKER, PORT)
mqttc.publish(TOPIC, MESSAGE)

while True:
    if GPIO.input(PUSH_BTN) == False:
        MESSAGE = "ON"
        mqttc.publish(TOPIC, MESSAGE)
        print("Published to " + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)
        
    else:
        MESSAGE = "FanOff"
        mqttc.publish(TOPIC, MESSAGE)
        print("Published to " + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)
    
mqttc.loop(2)
        
    
