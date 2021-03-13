import board
import digitalio
import busio
import time
import datetime
import paho.mqtt.client as mqtt
from datetime import datetime


#from adafruit_bmp280 import Adafruit_BMP280_I2C
import adafruit_bmp280

# Establecemos os parámetros do servidor MQTT
broker_IP="IP_SERVIDOR_MQTT"
client = mqtt.Client("RaspiBMP")

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
bmp280.mode = adafruit_bmp280.MODE_FORCE

# change this to match the location's pressure (hPa) at sea level
bmp280.seaLevelhPa = 1013.25
#bmp280.seaLevelhPa = 1037.8

# Iniciamos o bucle de toma de datos e comunicacion
while True:
        # Establecemos a conexion
        client.connect(broker_IP)

        # Facemos lectura da temperatura e humidade:
        pressure = bmp280.pressure
        temperature = bmp280.temperature
        altitude = bmp280.altitude

        # Obtemos a data e o momento de lectura
        now = datetime.now()
        now_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # Publicamos mensaxes coa temperatura bmp280 e humidade

        # Mensaxe de topic simple simple con valor de temperatura
        client.publish("casa/estudio2/temperatura","{0:0.1f}".format(temperature),qos=0,retain=True)


        # Mensaxe de topic simple simple con valor de presion
        client.publish("casa/estudio2/presion","{0:0.1f}".format(pressure),qos=0,retain=True)

        # Esperamos 5 minutos para volver executar o script
        time.sleep(300)
