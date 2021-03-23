import RPi.GPIO as GPIO
import os
from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer


host_name = '172.20.10.3'  # Change this to your Raspberry Pi IP address
host_port = 8000

    
class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command
            'curl -I http://server-ip-address:port'
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """ do_GET() can be tested using curl command
            'curl http://server-ip-address:port'
        """
        html = '''
           <html>
           <body style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <p>Current GPU temperature is {}</p>
           <p>Turn LED:
           <button><a href="/led/on">On</a></button>
           <button><a href="/led/off">Off</a></button></p>
           <div id="led-status"></div>
           
           <p>Turn Fan:
           <button><a href="/fan/on">On</a></button>
           <button><a href="/fan/off">Off</a></button></p>
           <div id="led-status"></div>
           <script>
               document.getElementById("led-status").innerHTML="{}";
           </script>
           </body>
           </html>
        '''
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        self.do_HEAD()
        status = ''
        redPin = 5
        greenPin = 6
        bluePin = 13
        if self.path=='/':
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            #set pins as outputs
            GPIO.setup(redPin,GPIO.OUT)
            GPIO.setup(greenPin,GPIO.OUT)
            GPIO.setup(bluePin,GPIO.OUT)

            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(20, GPIO.OUT)
        elif self.path=='/led/on':
            GPIO.output(redPin,GPIO.LOW)
            GPIO.output(greenPin,GPIO.LOW)
            GPIO.output(bluePin,GPIO.LOW)
            status='LED is On'
        elif self.path=='/led/off':
            GPIO.output(redPin,GPIO.HIGH)
            GPIO.output(greenPin,GPIO.HIGH)
            GPIO.output(bluePin,GPIO.HIGH)
            status='LED is Off'
        elif self.path=='/fan/on':
            GPIO.output(20, GPIO.LOW)
            status='Fan is On'
        elif self.path=='/fan/off':
            GPIO.output(20, GPIO.HIGH)
            status='Fan is Off'
        self.wfile.write(html.format(temp[5:], status).encode("utf-8"))


if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()