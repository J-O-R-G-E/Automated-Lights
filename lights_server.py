#!/usr/bin/python3

"""
This program is for web services and integration with ITTT/Google Home.

"""


##
# Source: https://www.e-tinkers.com/2018/04/how-to-control-raspberry-pi-gpio-via-http-web-server/
##
import RPi.GPIO as GPIO
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep

host_name = '' 
host_port = 8090

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
                
                html = ""
                self.do_HEAD()
                if self.path=='/':
                        html = '''
                        <html>
                        <body style="width:960px; margin: 20px auto;">
                        <h1>Front Lights Home Page</h1>
                        <h3>Current GPU temperature is {}</h3>
                        </body>
                        </html>
                        '''
                        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
                        self.wfile.write(html.format(temp[5:]).encode("utf-8"))

                        #output = subprocess.check_output("/opt/vc/bin/vcgencmd measure_temp", shell=True)
                        #outpu[5:-1]
                        return
                
                elif self.path=='/on':
                        html = '''
                        <html>
                        <body style="width:960px; margin: 20px auto;">
                        <h1>Front Lights Server</h1>
                        <h3>Turning front lights on... <h3>
                        </body>
                        </html>
                        '''

                        pinNum = 23
                        GPIO.setmode(GPIO.BCM)
                        GPIO.setwarnings(False)
                        GPIO.setup(pinNum,GPIO.OUT)
                        GPIO.output(pinNum,0)
                        #print("Turned On...")

                        sleep(1)
                        
                        pinNum = 24
                        GPIO.setmode(GPIO.BCM)
                        GPIO.setwarnings(False)
                        GPIO.setup(pinNum,GPIO.OUT)
                        GPIO.output(pinNum,0)
                        #print("Turned On...")
        
                elif self.path=='/off':
                        html = '''
                        <html>
                        <body style="width:960px; margin: 20px auto;">
                        <h1>Front Lights Server</h1>
                        <h3>Turning front lights off...  <h3>
                        </body>
                        </html>
                        '''

                        pinNum = 23
                        GPIO.setmode(GPIO.BCM)
                        GPIO.setwarnings(False)
                        GPIO.setup(pinNum,GPIO.OUT)
                        GPIO.output(pinNum,1)
                        #print("Turned Off...")

                        sleep(1)
                        
                        pinNum = 24
                        GPIO.setmode(GPIO.BCM)
                        GPIO.setwarnings(False)
                        GPIO.setup(pinNum,GPIO.OUT)
                        GPIO.output(pinNum,1)
                        #print("Turned Off...")

                elif self.path=='/status':
                        GPIO.setmode(GPIO.BCM)
                        GPIO.setwarnings(False)
                        GPIO.setup(23, GPIO.OUT)
                        porch = not GPIO.input(23)
                        if not porch:
                                porch = "Off"
                        else:
                                porch = "On"
                                
                                
                        GPIO.setmode(GPIO.BCM)
                        GPIO.setwarnings(False)
                        GPIO.setup(24, GPIO.OUT)
                        outside = not GPIO.input(24)
                        if not outside:
                                outside = "Off"
                        else:
                                outside = "On"
                                
                        html = '''
                        <html>
                        <body style="width:960px; margin: 20px auto;">
                        <h1>Front Lights Home Page</h1>
                        <h3> Porch Lights:   {}</h3>
                        <h3> Outside Lights: {}</h3>
                        </body>
                        </html>
                        '''
                        self.wfile.write(html.format(porch, outside).encode("utf-8"))
                        return

                elif self.path=='/notify':
                        os.system("../camara/Notification/./camara_notification.py")
                        return
                else:
                        html = '''
                        <html>
                        <body style="width:960px; margin: 20px auto;">
                        <h1>Front Lights Server</h1>
                        <h3>ERROR: Invalid path...  <h3>
                        </body>
                        </html>
                        '''

                #self.wfile.write(html.format(temp[5:], status).encode("utf-8"))
                self.wfile.write(html.encode("utf-8"))


if __name__ == '__main__':
        http_server = HTTPServer((host_name, host_port), MyServer)
        print("Server Starts - %s:%s" % (host_name, host_port))
        
        try:
                http_server.serve_forever()
        except KeyboardInterrupt:
                http_server.server_close()
