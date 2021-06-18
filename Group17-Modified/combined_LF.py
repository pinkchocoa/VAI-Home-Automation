#Thingspeak
from urllib.request import urlopen

#Light
import RPi.GPIO as GPIO, time, os
import time

GPIO.setmode(GPIO.BCM)
#Fan
import smbus
    
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

#set red,green and blue pins
redPin = 5
greenPin = 6
bluePin = 13

#set pins as outputs
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

#Select GPIO Mode
GPIO.setmode(GPIO.BCM)
#set red,green and blue pins
redPin = 5
greenPin = 6
bluePin = 13
#set pins as outputs
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

def turnOff():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)
    
def white():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.LOW)
    
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

while True:
    #Light
    print (RCtime(17))
    
    #Fan
    temperature = read_temp()
    
    print(round(temperature, 2), "C")
    time.sleep(1)
    
    if (RCtime(17)) > 6000:
        #Light
        white()
        
        #Light
        print("Led On")
        
    else:
        #Light
        turnOff()
        print("Led Off")
    

    if temperature > 29.00:
        #Fan
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        FAN_PIN = 20
       
        GPIO.setup(FAN_PIN, GPIO.OUT)
        GPIO.output(FAN_PIN, GPIO.LOW)
       
        #Fan
        time.sleep(0.5)
        
    else:
        #Fan
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        FAN_PIN = 20
        GPIO.setup(FAN_PIN, GPIO.OUT)
        GPIO.output(FAN_PIN, GPIO.HIGH)