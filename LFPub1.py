import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LED_PIN1 = 16
GPIO.setup(LED_PIN1, GPIO.OUT)

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
        
        GPIO.output(LED_PIN1, True)
  
        ledState = True
        
        MESSAGE = 'On'
        mqttc.publish(TOPIC, MESSAGE)
        
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)
        
    elif buttonPress == False and ledState == True:
        GPIO.output(LED_PIN1, False)
  
        ledState = False
        
        MESSAGE = 'Off'
        mqttc.publish(TOPIC, MESSAGE)
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)

        
mqttc.loop(2)
