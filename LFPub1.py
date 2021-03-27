import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO, time, os
import time
from time import sleep
from audio.micRec import micRec
import smbus
from audio.recordSound import recordSound, transribeSound
from audio.speakText import speakText

GPIO.setmode(GPIO.BCM)
    
#Temp
i2c_ch = 1
i2c_address = 0x48
reg_temp = 0x00
reg_config = 0x01

def twos_comp(val, bits):
    if (val & (1 << (bits-1))) != 0:
        val = val-(1<<bits)
    return val

def read_temp():
    val = bus.read_i2c_block_data(i2c_address, reg_temp, 2)
    temp_c = (val[0] << 4) | (val[1] >> 5)

    temp_c = twos_comp(temp_c, 12)

    temp_c = temp_c * 0.0625

    return temp_c

bus = smbus.SMBus(i2c_ch)

val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
print ("Old CONFIG:", val)

val[1] = val[1] & 0b00111111
val[1] = val[1] | (0b10 << 6)

bus.write_i2c_block_data(i2c_address, reg_config,val)

val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
print("New CONFIG:", val)

#Light
def RCtime (RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.5)
    GPIO.setup(RCpin, GPIO.IN)
    while (GPIO.input(RCpin) == GPIO.LOW):
           reading += 1
    return reading

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
    #Light
    print (RCtime(17))
    
    #Fan
    temperature = read_temp()
    
    print(round(temperature, 2), "C")
    time.sleep(1)
    
    said = micRec(3)
    if checkVoiceInput(said, ['light', 'on']) or (RCtime(17)) > 6000:
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
    
    elif checkVoiceInput(said, ["send", "message"]):
        MESSAGE = 'Record Voice'
        speakText('recording voice')
        recordSound('output', 10)
        MESSAGE += transribeSound('output')
        mqttc.publish(TOPIC, MESSAGE)
        print('Published to ' + MQTTBROKER + ': ' + TOPIC + ':' + MESSAGE)
        time.sleep(1)
        
mqttc.loop(2)
