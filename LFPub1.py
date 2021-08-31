import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO, time, os
import time
from time import sleep
from audio.micRec import micRec
import smbus
from audio.recordSound import recordSound, transribeSound
from audio.speakText import speakText
from fileio import file_to_set, write_file, append_to_file, delete_file_contents

def checkInput(said, inputs):
    if said is None or not said:
#         print("Nothing is said")
        return False
    print("You said this: " + str(said))
    for x in inputs:
        if x not in said:
            return False
    return True

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

FAN_PIN1 = 20
GPIO.setup(FAN_PIN1, GPIO.OUT)
GPIO.setup(FAN_PIN1, True)

def turnOff():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)
    
def white():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.LOW)

turnOff()

LIGHT_BTN = 18
GPIO.setup(LIGHT_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

FAN_BTN = 26
GPIO.setup(FAN_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
MQTTBROKER = 'test.mosquitto.org'
PORT = 1883
TOPIC = 'home/light'
MESSAGE = 'CONNECTED'
mqttc = mqtt.Client('python_pub')
mqttc.connect(MQTTBROKER, PORT)
mqttc.publish(TOPIC, MESSAGE)

while True:

    said = micRec(3)
    #check textfile
    textfile = 'status.txt'
    content = file_to_set (textfile)
    print(content)
    for i in content:
        if i == "":
            continue
        else:
            content = i
            break
        print(content)

    if checkInput(said, ['light', 'on']) or checkInput(content, ['LED', 'On']):
        #reset variable
        white()
        MESSAGE = 'Light On'
        mqttc.publish(TOPIC, MESSAGE)
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(2)
        
            
    elif checkInput(said, ["light", "off"]) or checkInput(content, ['LED', 'Off']):
        turnOff()
        MESSAGE = 'Light Off'
        mqttc.publish(TOPIC,MESSAGE)
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(2)
        
    
    elif checkInput(said, ["fan", "on"]) or checkInput(content, ['Fan', 'On']):
        
        GPIO.output(FAN_PIN1, False)
        MESSAGE = 'Fan On'
        mqttc.publish(TOPIC, MESSAGE)
        
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(2)
        
    elif checkInput(said, ["fan", "off"]) or checkInput(content, ['Fan', 'Off']):
        GPIO.output(FAN_PIN1,True )
        MESSAGE = 'Fan Off'
        mqttc.publish(TOPIC,MESSAGE)
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(2)
    
    elif checkInput(said, ["send", "message"]):
        MESSAGE = 'Record Voice'
        speakText('recording voice')
        recordSound('output', 10)
        speakText('message sent')
        MESSAGE += transribeSound('output')
        mqttc.publish(TOPIC, MESSAGE)
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(2)
    print("deleting contents...")
    print(content)
    delete_file_contents(textfile)        
mqttc.loop(1)

