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

count = 0

while True:
    #Light
    print (RCtime(18))
    GPIO.setup(26,GPIO.OUT)
    #GPIO.setup(20,GPIO.OUT)
    ldrdata = urlopen("https://api.thingspeak.com/update?api_key=WMHWC7KXM98IY9EK&field3=" + str(RCtime(18)))
    ldrdata.close()
    #Fan
    temperature = read_temp()
    #ThingSpeak
    data1 = urlopen("https://api.thingspeak.com/update?api_key=WMHWC7KXM98IY9EK&field1=" + str(temperature))
    data1.close()
    
    print(round(temperature, 2), "C")
    time.sleep(1)
    
    if (RCtime(18)) > 6000:
        #Light
        GPIO.setwarnings(False)
        GPIO.output(26, GPIO.HIGH)
        #GPIO.output(20, GPIO.HIGH)
        #Light
        print("Led On")
        
    else:
        #Light
        GPIO.output(26, GPIO.LOW)
        #GPIO.output(20, GPIO.LOW)
        print("Led Off")
    

    if temperature > 23.00:
        #Fan
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        FAN_PIN = 16
        #FAN_PIN1 = 12
        GPIO.setup(FAN_PIN, GPIO.OUT)
        GPIO.output(FAN_PIN, True)
        count = count+1
        data2 = urlopen("https://api.thingspeak.com/update?api_key=1DAY7XC8O4PYM4MS&field1=" + str(count))
        data2.close()
        print(count, "times turned on")
        #GPIO.setup(FAN_PIN1, GPIO.OUT)
        #GPIO.output(FAN_PIN1, True)
        #GPIO.output(6, GPIO.HIGH)
        #Fan
        time.sleep(0.5)
        
    else:
        #Fan
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        FAN_PIN = 16
        #FAN_PIN1 = 12
        GPIO.setup(FAN_PIN, GPIO.OUT)
        GPIO.output(FAN_PIN, False)
        #GPIO.setup(FAN_PIN1, GPIO.OUT)
        #GPIO.output(FAN_PIN1, False)
        
        
