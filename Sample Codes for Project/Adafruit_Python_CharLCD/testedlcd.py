import RPi.GPIO as GPIO
import sys
import urllib2
from time import sleep
import Adafruit_DHT as dht

# LCD
import Adafruit_CharLCD as LCD

#Relay
GPIO.setmode(GPIO.BCM)
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)


# Raspberry PI connections
lcd_rs		= 27	# Older versions if not working change to 21
lcd_en		= 22
lcd_d4		= 25
lcd_d5		= 24
lcd_d6		= 23
lcd_d7		= 18
lcd_backlight	= 4

# Define some device constants
lcd_columns	= 16
lcd_rows	= 2

# Initialize the LCD
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

#Thingspeak
# Enter Your API key here
myAPI = 'WMHWC7KXM98IY9EK' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

def DHT22_data():
	# Reading from DHT22 and storing the temperature and humidity
	humi, temp = dht.read_retry(dht.DHT22, 20) 
	return humi, temp

while True:
	try:
            humi, temp = DHT22_data()
            
	    # If Reading is valid
            if isinstance(humi, float) and isinstance(temp, float):
                
                # Formatting to two decimal places
                humi = '%.2f' % humi 					   
                temp = '%.2f' % temp
	    
                # clear lcd
                lcd.clear()

                # display temperature
                lcd.message ("Temperature:\n")
	
                # Mostrar a temperatura quase no final
                toMove = lcd_columns - len(temp)
                lcd.set_cursor(toMove,1)
                lcd.message(temp)

                sleep(2) # 5 second delay
                lcd.clear()
                # display humidity
                lcd.message ("Humidity:\n")
                toMove = lcd_columns - len(humi)
                lcd.set_cursor(toMove,1)
                lcd.message (humi)
	    
            
                # Sending the data to thingspeak
                conn = urllib2.urlopen(baseURL + '&field2=%s' % (humi))
                print (humi)
                # Closing the connection
##                conn.close()
	    
                #sleep(2)
	except KeyboardInterrupt:
	    lcd.clear()
	    lcd.message("Adeus!")
	    time.sleep(1)
	    sys.exit()
	    
	  
