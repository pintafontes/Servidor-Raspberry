# O sensor CCS811 mide a concentración de certos volátiles orgánicos (tvoc) e mediante un modelo descoñecido deduce a concentración de CO2 equivalente (eco2)
import time
import board
import busio
import adafruit_ccs811

### Engadidos para facer o script MQTT
import digitalio
import paho.mqtt.client as mqtt

### Establecemos os parámetros do servidor MQTT
broker_IP="IP_SERVIDOR_MQTT"
client = mqtt.Client("RaspiCCS811")

i2c = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c)

# Establecemos a conexion
client.connect(broker_IP)

# Wait for the sensor to be ready
while not ccs811.data_ready:
    pass

while True:
    print("CO2: {} PPM, TVOC: {} PPB".format(ccs811.eco2, ccs811.tvoc)) # Impresion en consola para diagnostico
    eco2 = ccs811.eco2
    tvoc = ccs811.tvoc
    # Mensaxe de topic simple simple con valor de temperatura
    client.publish("casa/estudio/eco2","{0:0.0f}".format(eco2),qos=0,retain=True)

    # Mensaxe de topic simple simple con valor de presion
    client.publish("casa/estudio/tvoc","{0:0.0f}".format(tvoc),qos=0,retain=True)

    # Esperamos 30 segundos para volver executar o script
    time.sleep(30)
