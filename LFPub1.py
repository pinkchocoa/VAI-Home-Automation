import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from time import sleep
from audio.micRec import micRec

def checkVoiceInput(said, inputs):
    
    if said is None:
        print("Nothing is said")
        return False
    print("You said this: " + said)
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

def turnOff():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)
    
def white():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.LOW)


LIGHT_BTN = 18
GPIO.setup(LIGHT_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

FAN_BTN = 26
GPIO.setup(FAN_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
MQTTBROKER = 'test.mosquitto.org'
PORT = 1883
TOPIC = 'home/light'
MESSAGE = 'ON'
mqttc = mqtt.Client('python_pub')
mqttc.connect(MQTTBROKER, PORT)
mqttc.publish(TOPIC, MESSAGE)

LightButtonPress = True
FanButtonPress = True
ledState = False
fanState = False


while True:
    LightButtonPress = GPIO.input(LIGHT_BTN)
    FanButtonPress = GPIO.input(FAN_BTN)
    
    said = micRec(3)
    if checkVoiceInput(said, ['light', 'on']):
   # if 'light' in said and 'on' in said:
        white()
        MESSAGE = 'Light On'
        mqttc.publish(TOPIC, MESSAGE)
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)
    
    elif checkVoiceInput(said, ["light", "off"]):
    #if 'light' in micRec() and 'off' in micRec():
        turnOff()
        MESSAGE = 'Light Off'
        mqttc.publish(TOPIC,MESSAGE)
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)
    
    elif checkVoiceInput(said, ["fan", "on"]):
        
        GPIO.output(FAN_PIN1, False)
        MESSAGE = 'Fan On'
        mqttc.publish(TOPIC, MESSAGE)
        
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)
        
    elif checkVoiceInput(said, ["fan", "off"]):
        GPIO.output(FAN_PIN1,True )
        MESSAGE = 'Fan Off'
        mqttc.publish(TOPIC,MESSAGE)
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)
        
mqttc.loop(2)
