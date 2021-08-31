import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from time import sleep
from audio.speakText import speakText

GPIO.setmode(GPIO.BCM)

redPin = 13
greenPin = 19
bluePin = 26

GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

FAN_PIN2 = 16
GPIO.setup(FAN_PIN2, GPIO.OUT)

def turnOff():
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.HIGH)
    
def white():
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.LOW)
    

MQTTBROKER = 'test.mosquitto.org'
PORT = 1883

def on_connect(client, userdata, flags, rc):
        print('Connected with result code ' + str(rc))
        client.subscribe('home/light')
        
def on_disconnect(client, userdata, rc):
    print('Disconnect with result code' + str(rc))
    
def on_message(client, userdata, msg):
    txt = str(msg.payload)
    txt = txt.split("'")[1]
    print("txt: ", txt)
    
    if 'Record Voice' in txt:
        txt=txt[len('Record Voice'):]
        print(txt)
    elif txt == 'Light On':
        white()
    elif txt == 'Light Off':
        turnOff()
    elif txt == 'Fan On':
        GPIO.output(FAN_PIN2, GPIO.HIGH)
    
    elif txt == 'Fan Off':
        GPIO.output(FAN_PIN2, GPIO.LOW)
        
    speakText(txt)
        
    print(MQTTBROKER + ': <' + msg.topic + '> :' + str(msg.payload))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTTBROKER, PORT)

client.loop_forever()

