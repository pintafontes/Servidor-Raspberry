<h1>Conectar un sensor HDC1080 (Humidade e Temperatura) na Raspberry PI</h1>
<p>Baseado en:</p>
    <ul>
        <li>https://github.com/switchdoclabs/SDL_Pi_HDC1000 para as librerías e software de testeo</li>
        <li>http://www.pibits.net/code/raspberry-pi-and-hdc1080-humidity-and-temperature-sensor.php para a descripción da conexión e o testeo de software</li>
        <li>https://learn.adafruit.com/adafruit-hdc1008-temperature-and-humidity-sensor-breakout/overview describe o hardware e a conexión a Arduino.</li>
        <li>http://www.esp8266learning.com/esp8266-hdc1080-humidity-temperature-sensor.php describe o hardware e a conexión a ESP8266</li>
</ul>
<h2>Conexión á Raspberry</h2>
Hai 4 cables:
Módulo HDC1080
Raspberry Pi
Node MCU
Arduino
Función

3v3/5v (Vermello)
GND (Negro)
SDA (Verde)
SCL (Amarelo)
3v3
GND
SDA – Pin 3
SCL – Pin 5
3v3
GND
SDA – D2
SCL – D1
3v3/5V
GND
SDA – A4
SCL – A5
Alimentación
Terra
Datos
Reloxo

É necesario instalar e activar diversas dependencias para traballar co BUS i2c, tal como se explica no apartado anterior para o sensor BMP. Resumindo, as ordes son:
# apt-get install -y python-smbus i2c-tools
# raspi-config 			<--acceder á opción 5 Interfacing Options e activar i2c
$ ls /dev/i2c* /dev/spi*		<--comprobar que o bus i2c é accesible
$ i2cdetect -y 1			<--comprobar que o sensor está no enderezo 0x40
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# pip3 install RPI.GPIO
# pip3 install adafruit-circuitpython-busdevice
    • A única biblioteca (AKA librería) dispoñible para poder interactuar cos sensores da familia HDC-10XX está na web https://github.com/switchdoclabs/SDL_Pi_HDC1000. Inclúe unha pequena peza de python2 para probar o sensor:
$ pi@raspberry1:~/HDC1080 $ python2 testHDC1000.py 
Test SDL_Pi_HDC1000 Version 1.1 - SwitchDoc Labs
Sample uses 0x40 and SwitchDoc HDC1000 Breakout board 
Program Started at:2020-11-15 12:52:35
------------
Manfacturer ID=0x5449
Device ID=0x1050
Serial Number ID=0x2177F80
configure register = 0x1000
turning Heater On
configure register = 0x3000
turning Heater Off
configure register = 0x1000
change temperature resolution
configure register = 0x1400
change temperature resolution
configure register = 0x1000
change humidity resolution
configure register = 0x1200
change humidity resolution
configure register = 0x1000
-----------------
Temperature = 19.4 C
Humidity = 87.2 %
-----------------
    • Tomando o seu código como referencia, temos este script hdc1080_mqtt.py para publicar as lecturas en MQTT, que colocaremos en /home/pi/IoT e o servizo /lib/systemd/system/hdc_mqtt.service que o inicia en cada arranque da máquina:
$ cat /home/pi/IoT/hdc1080_mqtt.py
#!/usr/bin/env python
# Baseado en Test SDL_Pi_HDC1000
# 
# June 2017
#imports
import sys
import time
import datetime
import SDL_Pi_HDC1000 #debe estar no mesmo cartafol que o script
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
        # Mensaxe de topic simple simple con valor de temperatura        client.publish("mendinho/hall/temperaturaHDC","{0:0.1f}".format(temperatura),qos=0,retain=True)
        # Mensaxe de topic simple simple con valor de presion
client.publish("mendinho/hall/humidadeHDC","{0:0.1f}".format(humidade),qos=0,retain=True)
        # Esperamos 5 minutos para volver executar o script
        time.sleep(300)
# cat /lib/systemd/system/hdc_mqtt.service
[Unit]
Description=HDC1080 Pressure and Temperature Sensor Reading and MQTT Communication
After=mosquitto.service
[Service]
Type=simple
Restart=always
RestartSec=1
User=pi
ExecStart=/usr/bin/python3 /home/pi/IoT/hdc1080_mqtt.py 
[Install]
WantedBy=multi-user.target
    • Rexistramos o servizo en Systemd, comprobamos o funcionamento e activamos o inicio automático:
# systemctl daemon-reload
# systemctl start hdc_mqtt.service 
# systemctl status hdc_mqtt.service
● hdc_mqtt.service - HDC 1080 Pressure and Temperature Sensor Reading and MQTT Communication
   Loaded: loaded (/lib/systemd/system/hdc_mqtt.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2020-11-15 10:11:03 GMT; 4h 4min ago
 Main PID: 24250 (python3)
    Tasks: 1 (limit: 2184)
   CGroup: /system.slice/hdc_mqtt.service
           └─24250 /usr/bin/python3 /home/pi/IoT/hdc1080_mqtt.py
Nov 15 10:11:03 raspberry1 systemd[1]: Started HDV1080 Pressure and Temperature [...]
# systemctl enable hdc_mqtt.service
