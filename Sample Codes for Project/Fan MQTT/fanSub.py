import paho.mqtt.client as mqtt

#Fan
import time
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
    
FAN_PIN = 16

#Enter the details for your MQTT broker
MQTTBROKER = 'iot.eclipse.org'
PORT = 1883

# The callback for when the client receives a CONNACK response from the server.
def on_connect (client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("home/doorbell")
    
def on_disconnect(client, userdata, rc):
    print("Disconnected with result code " + str(rc))
    
# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    
    
    if str(msg.payload)=="ON":
        GPIO.setup(FAN_PIN, GPIO.OUT)
        GPIO.output(FAN_PIN, True)
        time.sleep(1)
        
    else:
        GPIO.setup(FAN_PIN, GPIO.OUT)
        GPIO.output(FAN_PIN, False)
           
    print(MQTTBROKER + ': <' + msg.topic + "> : " + str(msg.payload))

    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect


client.connect(MQTTBROKER, PORT)

#Blocking call the processes network traffic, dispatches callbacks and
#handles reconnecting.
#other loop*() functions are available that give a threaded interface and a
#manual interface.

client.loop_forever()