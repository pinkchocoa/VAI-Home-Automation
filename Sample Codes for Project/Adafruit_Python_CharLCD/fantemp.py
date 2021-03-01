#Temp
from urllib.request import urlopen
import time
import smbus
import RPi.GPIO as GPIO

#Relay
# setting a current mode
GPIO.setmode(GPIO.BCM)
#removing the warings 
GPIO.setwarnings(False)
#creating a list (array) with the number of GPIO's that we use 
pins = [14]

GPIO.setup(pins, GPIO.OUT)

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

while True:
    temperature = read_temp()
    data1 = urlopen("https://api.thingspeak.com/update?api_key=WMHWC7KXM98IY9EK&field1=" + str(temperature))
    data1.close()
    print(round(temperature, 2), "C")
    time.sleep(1)

#Fan On
    if temperature>27.00:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        FAN_PIN = 24
        #FAN_PIN2 = 21
        #GPIO.setup(FAN_PIN2, GPIO.OUT)
        GPIO.setup(FAN_PIN, GPIO.OUT)
        #GPIO.output(FAN_PIN2, True)
        GPIO.output(FAN_PIN, True)

#Fan Off
    else:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        FAN_PIN = 24
        #FAN_PIN2 = 21
        #GPIO.setup(FAN_PIN2, GPIO.OUT)
        GPIO.setup(FAN_PIN, GPIO.OUT)
        #GPIO.output(FAN_PIN2, False)
        GPIO.output(FAN_PIN, False)
        
        #data4 = urlopen("https://api.thingspeak.com/update?api_key=WMHWC7KXM98IY9EK&field4=" + str(GPIO.input(25)))
        #data4.close()
        time.sleep(1)
        
for pin in reversed(pins) :
	GPIO.output(pin,  GPIO.HIGH)
