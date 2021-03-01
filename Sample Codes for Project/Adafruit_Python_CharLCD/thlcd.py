#import libraries
from urllib.request import urlopen
from time import sleep
import RPi.GPIO as GPIO
import time
import sys
# DHT sensor
import Adafruit_DHT

# LCD
import Adafruit_CharLCD as LCD

# Define sensor
sensor = Adafruit_DHT.AM2302
pin = 6

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

while True:
	try:
		# Get values
		humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)

		temp = "{:0.1f}*C".format(temperature)
		hum = "{:0.1f}%".format(humidity)

		# clear lcd
		lcd.clear()

		# display temperature
		lcd.message ("Temperatura:\n")
	
		# Mostrar a temperatura quase no final
		toMove = lcd_columns - len(temp)
		lcd.set_cursor(toMove,1)
		lcd.message(temp)

		time.sleep(2) # 5 second delay
		lcd.clear()
		# display humidity
		lcd.message ("Humidity:\n")
		toMove = lcd_columns - len(hum)
		lcd.set_cursor(toMove,1)
		lcd.message (hum)
		time.sleep(2)

	except KeyboardInterrupt:
		lcd.clear()
		lcd.message("Adeus!")
		time.sleep(1)
		sys.exit()
