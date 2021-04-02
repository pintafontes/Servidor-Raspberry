# Conectar un sensor HDC1080 (Humidade e Temperatura) na Raspberry PI
Baseado en:

* https://github.com/switchdoclabs/SDL_Pi_HDC1000 para as librerías e software de testeo
* http://www.pibits.net/code/raspberry-pi-and-hdc1080-humidity-and-temperature-sensor.php para a descripción da conexión e o testeo de software
* https://learn.adafruit.com/adafruit-hdc1008-temperature-and-humidity-sensor-breakout/overview describe o hardware e a conexión a Arduino.
* http://www.esp8266learning.com/esp8266-hdc1080-humidity-temperature-sensor.php describe o hardware e a conexión a ESP8266

## Conexión á Raspberry, NodeMCU ou Arduino
### Cableado
Hai 4 cables que unen o sensor HDC1080 co porto I2C. Dous son para a alimentación e outros dous para a transmisión de datos. Resulta bastante práctico para isto usar cable telefónico de 4 fios, que se pode estender varios metros sen problema, aínda que as unións son un pouco fráxiles:
Módulo HDC1080 | Raspberry Pi | Node MCU | Arduino | Función
------------ | -------------| -------------| -------------| -------------
3v3/5v (Vermello)  | 3v3 | 3v3| 3v3 | Alimentación
GND (Negro) | GND | GND | GND |Terra
S __D__ A (Verde) | SDA – Pin 3  | SDA – D2 | SDA – A4 | Datos ( __D__ ata)
S __C__ L (Amarelo) | SCL – Pin 5 | SCL – D1 | SCL – A5 | Reloxo (__C__ lock)

### Software 
É necesario instalar e activar diversas dependencias para traballar co BUS i2c, tal como se explica no apartado anterior para o sensor BMP. Resumindo, as ordes son:

`# apt-get install -y python-smbus i2c-tools`

`# raspi-config`        <-- acceder á opción 5 Interfacing Options e activar i2c

`$ ls /dev/i2c* /dev/spi*`		<--comprobar que o bus i2c é accesible

`$ i2cdetect -y 1`			<--comprobar que o sensor está no enderezo 0x40

    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

`# pip3 install RPI.GPIO `

`# pip3 install adafruit-circuitpython-busdevice `

A única biblioteca (AKA librería) dispoñible para poder interactuar cos sensores da familia HDC-10XX está na web https://github.com/switchdoclabs/SDL_Pi_HDC1000. Inclúe unha pequena peza de python2 para probar o sensor:

`$ pi@raspberry1:~/HDC1080 $ python2 testHDC1000.py `

    Test SDL_Pi_HDC1000 Version 1.1 - SwitchDoc Labs
    Sample uses 0x40 and SwitchDoc HDC1000 Breakout board 
    Program Started at:2020-11-15 12:52:35
    ------------
    Manfacturer ID=0x5449
    Device ID=0x1050
    Serial Number ID=0x2177F80
    [...]
    -----------------
    Temperature = 19.4 C
    Humidity = 87.2 %
    -----------------
Tomando ese código como referencia, fixen o script [hdc1080_mqtt.py](sensors/hdc1080_mqtt.py) para publicar as lecturas en MQTT, que colocaremos en `/home/pi/sensors`, así como o servizo [hdc_mqtt.service](services/hdc_mqtt.service) que colocaremos en `/lib/systemd/system/` e que se encarga de iniciar o script en cada arranque da máquina.
os datos son publicados nos _topic_ `casa/salon/temperaturaHDC` e  `casa/salon/humidadeHDC` cada 5 minutos.

### Activación do servizo
Rexistramos o servizo en Systemd, comprobamos o funcionamento e activamos o inicio automático:

`# systemctl daemon-reload`

`# systemctl start hdc_mqtt.service`

`# systemctl status hdc_mqtt.service`

    hdc_mqtt.service - HDC 1080 Pressure and Temperature Sensor Reading and MQTT Communication
    Loaded: loaded (/lib/systemd/system/hdc_mqtt.service; enabled; vendor preset: enabled)
    Active: active (running) since Sun 2020-11-15 10:11:03 GMT; 4h 4min ago
    Main PID: 24250 (python3)
    Tasks: 1 (limit: 2184)
    CGroup: /system.slice/hdc_mqtt.service
           └─24250 /usr/bin/python3 /home/pi/sensors/HDC1080_mqtt.py
    Nov 15 10:11:03 raspberry1 systemd[1]: Started HDV1080 Pressure and Temperature [...]

`# systemctl enable hdc_mqtt.service`

