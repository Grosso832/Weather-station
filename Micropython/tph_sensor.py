from machine import Pin, I2C
import time
import bme280_i2c
from display import *
import ntptime

device_name = 1

#Setting up time:
ntptime.settime()

#BME280
i2c_bme = I2C(0, scl=Pin(22), sda=Pin(21))
bme = bme280_i2c.BME280_I2C(0x76, i2c_bme)
bme.set_measurement_settings({
    'filter': bme280_i2c.BME280_FILTER_COEFF_OFF,
    'osr_h': bme280_i2c.BME280_OVERSAMPLING_1X,
    'osr_p': bme280_i2c.BME280_OVERSAMPLING_1X,
    'osr_t': bme280_i2c.BME280_OVERSAMPLING_1X})

pressure_fit = 1031.0 / 973 #1.058


def show_results(temp, humidity, pressure):
    oled.fill(0) #Bildschirm löschen
    text_line("Temp.: {:5.1f} C".format(temp), 1);
    text_line("Humidity: {:3.0f} %".format(humidity), 3);
    text_line("Press: {:5.0f} hPa".format(pressure), 5);
    oled.show()
    
def bme_measure():
    bme.set_power_mode(bme280_i2c.BME280_FORCED_MODE)
    time.sleep_ms(40)
    result = bme.get_measurement()
    return result["temperature"], result["humidity"], pressure_fit * result["pressure"] / 100

def create_sensordata():
    
    temp, humidity, pressure = bme_measure()
    sensordata = {'name':device_name, 'temperature':temp, 'humidity':humidity, 'pressure':pressure}
    return sensordata