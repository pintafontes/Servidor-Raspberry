#!/usr/bin/env python
#
# Test SDL_Pi_HDC1000
#
# June 2017
#

#imports

import sys          
import time
import datetime
import SDL_Pi_HDC1000

### Engadidos para facer o script MQTT
import board
import digitalio
import busio
import paho.mqtt.client as mqtt

### Establecemos os parámetros do servidor MQTT
broker_IP="192.168.1.10"
client = mqtt.Client("RaspiHDC1080")

# Main Program
hdc1000 = SDL_Pi_HDC1000.SDL_Pi_HDC1000()
hdc1000.turnHeaterOn() 
hdc1000.turnHeaterOff() 
hdc1000.setTemperatureResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_TEMPERATURE_RESOLUTION_11BIT)
hdc1000.setTemperatureResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
hdc1000.setHumidityResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_HUMIDITY_RESOLUTION_8BIT)
hdc1000.setHumidityResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT)
### Iniciamos o bucle de toma de datos e comunicacion
while True:
        # Establecemos a conexion
        client.connect(broker_IP)

        # Facemos lectura da temperatura e humidade:
        temperatura = hdc1000.readTemperature()
        humidade = hdc1000.readHumidity()

        # Mensaxe de topic simple simple con valor de temperatura
        client.publish("casa/estudio/temperaturaHDC","{0:0.1f}".format(temperatura),qos=0,retain=True)


        # Mensaxe de topic simple simple con valor de presion
        client.publish("casa/estudio/humidadeHDC","{0:0.1f}".format(humidade),qos=0,retain=True)

        # Esperamos 5 minutos para volver executar o script
        time.sleep(300)

