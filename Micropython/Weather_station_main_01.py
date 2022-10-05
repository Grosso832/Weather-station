import display as dp
from connection4 import *
from tph_sensor import *
from network_credentials import *
import socket
import json
import esp
from microWebSrv import MicroWebSrv
from openweathermap20_to_bme import *
from website import startHTTP, log, hp, wetter, create_sens

esp.osdebug(None)


def zeige_wetter():
    messzeit = aktuell.get_messzeit_text()
    
    wetter.clear()
    wetter.add("Aktuelles Wetter in {}, {}: {}".format(aktuell.get_ort_name(),aktuell.get_land(),aktuell.get_data_idx("weather",0,"description")))
    wetter.add("Gemessen am {}".format(messzeit))
    wetter.add()
    wetter.add("Temperatur:   {} Grad".format(aktuell.get_data("main","temp")))
    wetter.add("Luftdruck:    {} hPa".format(aktuell.get_data("main","pressure")))
    wetter.add("Feuchtigkeit: {} %".format(aktuell.get_data("main","humidity")))
    wetter.add()
    wetter.add("Wind:")
    wetter.add("Geschwindigkeit: {} m/s".format(aktuell.get_data("wind","speed")))
    wetter.add("Richtung:        {} Grad".format(aktuell.get_data("wind","deg")))
    
def homepage():
    ip = wifi.get_ip()
    hp.add("Die ESP32 - Wetterstation kennt momentan folgende Funktionen:")
    hp.add()
    hp.add('Das aktuelle Wetter: <a href="http://{}/wetter">http://{}/wetter</a>'.format(ip,ip))
    hp.add('Ein LOG als Debug-Hilfe beim Programmieren: <a href="http://{}/log">http://{}/log</a>'.format(ip,ip))
    

dp.oled.fill(0) # Bildschirm löschen
dp.text_line("Mit Netzwerk",1)
dp.text_line("verbinden...",2)
dp.oled.show();
#log.add_log("Mit WLAN verbinden...");

if wifi.connect(wlan_ssid,wlan_passwort):
    dp.oled.fill(0) # Bildschirm löschen
    dp.text_line(wifi.get_ssid(),1)
    dp.text_line(wifi.get_ip(),2)
    dp.oled.show()
    time.sleep(15)
    startHTTP()
    #log.add_log("Mit {} verbunden, IP-Adresse {}".format(wifi.get_ssid(),wifi.get_ip()))
    homepage()
    while True:
        temp, humidity, pressure = bme_measure()
        show_results(temp, humidity, pressure)
        time.sleep(1)

        
else:
    dp.oled.fill(0) # Bildschirm löschen
    dp.text_line("Kein Netzwerk",1)
    dp.text_line("gefunden!",2)
    dp.oled.show()
    #log.add_log("Keine Verbindung möglich")
    #log.print()


# while True:
#    temp, humidity, pressure = bme_measure()
#    show_results(temp, humidity, pressure)
#    time.sleep(5)