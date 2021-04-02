#!/usr/bin/python
import sys
import time
import datetime
import Adafruit_DHT as dht
import paho.mqtt.client as mqtt

# Establecemos os parámetros do sensor DHT
sensor = dht.DHT22
pin = 4

# Establecemos os parámetros do servidor MQTT
broker_IP="IP_SERVIDOR_MQTT"
client = mqtt.Client("RaspiDHT")

while True:
        # Establecemos a conexion
        client.connect(broker_IP)

        # Facemos lectura da temperatura e humidade:
        humidity, temperature = dht.read_retry(sensor, pin)

        # Publicamos mensaxes coa temperatura e humidade

        # Mensaxe de topic simple simple con valor de temperatura
        client.publish("casa/estudio1/temperatura","{0:0.1f}".format(temperature),qos=0,retain=True)
        time.sleep(0.1)

        # Mensaxe de topic simple simple con valor de humidade
        client.publish("casa/estudio1/humidade","{0:0.1f}".format(humidity),qos=0,retain=True)
        time.sleep(0.1)

        # Esperamos 5 minutos para volver executar o script
        time.sleep(300)
