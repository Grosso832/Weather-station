''' 
  Micropython mit ESP32
  Wetterdaten bei OpenWeatherMap beziehen
  
  Version 2.0, 27.05.2020
  Der Hobbyelektroniker
  https://community.hobbyelektroniker.ch
  https://www.youtube.com/c/HobbyelektronikerCh
  Der Code kann mit Quellenangabe frei verwendet werden.
'''

from connection3 import *
import socket
from network_credentials import *
import json
import time
import ntptime
from website import log

class WeatherWebService:
    
    _messzeit = 0
    _zeitzone = 0
    _ort_id = 0
    _ort_name = ""
    _land = ""
    _app_id = ""
    
    def __init__(self):
        self.js = []

    def get_request_string(self):
        return ""
    
    def request_data(self):
        return wifi.get_request(self.get_request_string()).json()
        #response = wifi.http_get(self.get_request_string())
        #lines = response.split("\r\n")
        #return json.loads(lines[-1])

    def get_json(self):
        return self.js

    def get_messzeit(self):
        return WeatherWebService._messzeit
    
    def get_messzeit_text(self):
        zeit = time.localtime(self.get_messzeit()-946684800+WeatherWebService._zeitzone)
        return "{:02d}.{:02d}.{:04d} {:02d}:{:02d}".format(zeit[2],zeit[1],zeit[0],zeit[3],zeit[4])
    
    def get_ort_name(self):
        return WeatherWebService._ort_name
        
    def get_land(self):
        return WeatherWebService._land
        
    def get_data(self,topic1,topic2="",topic3=""):
        try:
            result = self.js[topic1]
            if topic2 != "":
                result = result[topic2]
            if topic3 != "":
                result = result[topic3]
            return result    
        except:
            return "---"
            
    def get_data_idx(self,topic1,idx = 0,topic2="",topic3=""):
        try:
            result = self.js[topic1][idx]
            if topic2 != "":
                result = result[topic2]
            if topic3 != "":
                result = result[topic3]
            return result    
        except:
            return "---"
   
class WetterAktuell(WeatherWebService):
    
    def __init__(self, app_id, ort_id, ort_name, land, refresh_rate=600 ):
        super().__init__()
        WeatherWebService._messzeit = 0
        WeatherWebService._zeitzone = 0
        WeatherWebService._app_id = app_id
        self.set_ort(ort_id,ort_name,land)
        self.refresh_rate = refresh_rate
        self.oldtime = 0
        self.nexttime = 0
        self.isnew = False
        
    def set_ort(self, ort_id, ort_name, land):
        WeatherWebService._ort_id = ort_id
        WeatherWebService._ort_name = ort_name
        WeatherWebService._land = land
        
    def get_request_string(self):
        return "http://api.openweathermap.org/data/2.5/weather?id={}&lang=de&units=metric&APPID={}".format(WeatherWebService._ort_id,WeatherWebService._app_id)

    def refresh(self, force = False):
        if force or self.nexttime==0 or wifi.get_seconds() >= self.nexttime:
            log.add_log("Neue Wetterdaten anfordern")
            self.js.clear()
            self.js = self.request_data()
            time = self.js["dt"]
            WeatherWebService._messzeit = time
            WeatherWebService._ort_name = self.get_data("name")
            WeatherWebService._land = self.get_data("sys","country")
            if self.oldtime == time:
                self.isnew = False
                log.add_log("Keine neuen Wetterdaten")
                self.nexttime += 60 # erst in einer Minute wieder versuchen
            else:
                log.add_log("Neuen Wetterdaten geladen")
                self.isnew = True
                self.oldtime = time
                # nächste Zeit feststellen (Python-Zeit)
                timezone = self.js["timezone"]
                wifi.set_timezone(timezone)
                self.nexttime = time-946684800+self.refresh_rate
                WeatherWebService._zeitzone = timezone
    
        else:
            self.isnew = False
        return self.isnew


    
   


    
    
            
        


