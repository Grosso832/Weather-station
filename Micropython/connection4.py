import network
import time
import socket
import urequests as requests
from network_credentials import *

class WiFi:
    
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.timezone = 3600
        time.sleep(0.5)
        self.wlan.active(False)
        time.sleep(0.5)
        self.wlan.active(True);
        time.sleep(0.5)
    
    def connect(self,ssid, passwort, timeout = 10000):
        if (self.wlan.isconnected):
            self.wlan.disconnect()
            time.sleep(0.5)
        self.wlan.connect(ssid,passwort)
        start = time.ticks_ms();
        while not self.wlan.isconnected() and start + timeout > time.ticks_ms():
            time.sleep(0.1)
        return self.wlan.isconnected()
    
    def isconnected(self):
        return self.wlan.isconnected()
        
    def get_wlan(self):
        return self.wlan
    
    def get_ip(self):
        conf = self.wlan.ifconfig() # (ip, subnet, gateway, dns)
        return conf[0]
    
    def get_ssid(self):
        return self.wlan.config('essid')
    
    def http_get(self, url):
        _, _, host, path = url.split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        response = ""
        while True:
            data = s.recv(100)
            if data:
                response += str(data, 'utf8')
            else:
                break
        s.close()
        return response

    
wifi = WiFi()