import Adafruit_DHT as dht    # Importing Adafruit library for DHT22
from time import sleep           # Impoting sleep from time library to add delay
try:
    while 1:                # Loop will run forever
        humidity, temperature = dht.read_retry(dht.DHT22, 4)  # Reading humidity and temperature
        if humidity is not None and temperature is not None:
        	print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        else:
       		print("Failed to retrieve data from humidity sensor")

# If keyboard Interrupt is pressed
except KeyboardInterrupt:
    pass  			# Go to next line

