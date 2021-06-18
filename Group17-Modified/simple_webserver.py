import RPi.GPIO as GPIO
import os
from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
from fileio import file_to_set, append_to_file


host_name = 'jas.local'  # Change this to your Raspberry Pi IP address
host_port = 8000

class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """
    data = set()
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
        #check textfile
        textfile = 'status.txt'
        
        if self.path=='/':
            pass
        elif self.path=='/led/on':
            status='LED is On'
        elif self.path=='/led/off':
            status='LED is Off'
        elif self.path=='/fan/on':
            status='Fan is On'
        elif self.path=='/fan/off':
            status='Fan is Off'
            
        append_to_file(textfile,status)
        content = file_to_set(textfile)
        print(content)
        print(status)
        self.wfile.write(html.format(temp[5:], status).encode("utf-8"))


if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
