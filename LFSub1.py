import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)


MQTTBROKER = 'test.mosquitto.org'
PORT = 1883

def on_connect(client, userdata, flags, rc):
        print('Connected with result code ' + str(rc))
        client.subscribe('home/light')
        
def on_disconnect(client, userdata, rc):
    print('Disconnect with result code' + str(rc))
    
def on_message(client, userdata, msg):
    
    
    print(MQTTBROKER + ': <' + msg.topic + '> :' + str(msg.payload))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTTBROKER, PORT)

client.loop_forever()
