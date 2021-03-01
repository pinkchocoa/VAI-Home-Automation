import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

#light
LED_PIN2 = 23
GPIO.setup(LED_PIN2, GPIO.OUT)

FAN_PIN2 = 19
GPIO.setup(FAN_PIN2, GPIO.OUT)

MQTTBROKER = 'iot.eclipse.org'
PORT = 1883

def on_connect(client, userdata, flags, rc):
        print('Connected with result code ' + str(rc))
        client.subscribe('home/light')
        
def on_disconnect(client, userdata, rc):
    print('Disconnect with result code' + str(rc))
    
def on_message(client, userdata, msg):
    
    if str(msg.payload) == 'On':
        #GPIO.output(LED_PIN1, GPIO.HIGH)
        GPIO.output(LED_PIN2, GPIO.HIGH)
        GPIO.output(FAN_PIN2, GPIO.HIGH)
        

    else:
        #GPIO.output(LED_PIN1, GPIO.LOW)
        GPIO.output(LED_PIN2, GPIO.LOW)
        GPIO.output(FAN_PIN2, GPIO.LOW)
    
    print(MQTTBROKER + ': <' + msg.topic + '> :' + str(msg.payload))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTTBROKER, PORT)

client.loop_forever()