import display as dp
from connection3 import *
from tph_sensor import *
from network_credentials import *
import socket
import json
import esp
from microWebSrv import MicroWebSrv

esp.osdebug(None)

mws = MicroWebSrv()

dp.oled.fill(0) 
dp.text_line("Connecting...",1)
dp.oled.show();

def startSRV():
    mws = MicroWebSrv(webPath='www/')
    mws.MaxWebSocketRecvLen = 256
    #mws.WebSocketThreaded = True
    mws.Start(threaded=True)

@MicroWebSrv.route("/test")
def srvHandler(httpClient, httpResponse, routeArgs = None):
    httpResponse.WriteResponseOK(
                                    headers = ({"Cache-Control":"no-cache"}),
                                    contentType = "text/html",
                                    contentCharset = "UTF-8",
                                    content = html("Hallo")
                                )
    
def srv_content(content):
    return """\
            <!DOCTYPE html>
            <html lang=eng>
                <head>
                    <meta charset="UTF-8" />
                    <meta http-equiv="refresh" content="60">
                    <title>TEST-SITE</title>
                </head>
                <body>
                    <h1>ESP Wetterstation</h1>
                    <h3>
                    {}
                    </h3>
                </body>
            </html>
            """.format(content)


if wifi.connect(wlan_ssid,wlan_passwort):
    dp.oled.fill(0)
    dp.text_line("Connection", 1)
    dp.text_line("established:",2)
    dp.text_line(wifi.get_ssid(),3)
    dp.text_line(wifi.get_ip(),4)
    startSRV()
    dp.text_line("Server started",5)
    dp.oled.show()
    time.sleep(3)

else:
    dp.oled.fill(0) # Bildschirm löschen
    dp.text_line("Kein Netzwerk",1)
    dp.text_line("gefunden!",2)
    dp.oled.show()


# while True:
#    temp, humidity, pressure = bme_measure()
#    show_results(temp, humidity, pressure)
#    time.sleep(5)