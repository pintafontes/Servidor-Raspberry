# Conectar un sensor BMP280 na Raspberry PI

* Baseado en https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/circuitpython-test

* Moitos destes sensores véndense coa interface I2C ou coa SPI. A primeira é mais versátil, mentres a segunda é mais rápida. Eu escollo a primeira (mais info https://www.lifewire.com/selecting-between-i2c-and-spi-819003)

* Permite usar Python para facer lecturas de temperatura e presión atmosférica no sensor.

* Hai que activar a interface I2C na Raspberry usando a ferramenta `raspi-config`, xa que está desactivada por defecto. O proceso pode ser algo complicado se non temos unha instalación fresca de Raspbian. Engado algúns comandos adicionais que me serviron para ir resolvendo os numerosos atrancos que me foron aparecendo:
[mais detalles en https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c]

Instalamos os paquetes `python-smbus` e `i2c-tools`

    # apt-get install -y python-smbus i2c-tools
    # raspi-config <-- acceder á opción 5 Interfacing Options


## Conexión PI <--> Sensor
### Cableado (vale tamén para NodeMCU ou Arduino)
Hai 4 cables que unen o sensor BMP280 co porto I2C. Dous son para a alimentación e outros dous para a transmisión de datos. Resulta bastante práctico para isto usar cable telefónico de 4 fios, que se pode estender varios metros sen problema, aínda que as unións son un pouco fráxiles:
Módulo BMP280 | Raspberry Pi | Node MCU | Arduino | Función
------------ | -------------| -------------| -------------| -------------
3v3/5v (Vermello)  | 3v3 | 3v3| 3v3 | Alimentación
GND (Negro) | GND | GND | GND |Terra
S __D__ A (Verde) | SDA – Pin 3  | SDA – D2 | SDA – A4 | Datos ( __D__ ata)
S __C__ L (Amarelo) | SCL – Pin 5 | SCL – D1 | SCL – A5 | Reloxo (__C__ lock)


### Software 
Comprobamos que todo funciona ben cos seguintes comandos:

    $ ls /dev/i2c* /dev/spi*
    ls: cannot access '/dev/spi*': No such file or directory
    /dev/i2c-1

A resposta informanos de que temos activado o bus i2c nº1, pero non o bus SPI (tal como esperábamos)

    $ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    [...]
    70: -- -- -- -- -- -- 76 --

Agora obtemos como resposta que temos un dispositivo conectado no enderezo 0x76

Instalamos os drivers de Adafruit na Raspberry a través duns paquetes PIP de Python. No meu caso a execución baixo o usuario normal ($) da erros, así que fíxeno co superusuario (#):

    $ sudo su
    # pip3 install RPI.GPIO
    # pip3 install adafruit-circuitpython-busdevice
    # pip3 install adafruit-circuitpython-bmp280
    # pip3 install adafruit-blinka

Tiven problemas diversos con algúns paquetes que se resolveron forzando algunha reinstalación

    # python3 -m pip install --force-reinstall adafruit-blinka

Podemos comprobar se todo foi ben executando o script-python de exemplo para probar a [biblioteca blinka de ADafruit](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)

    $ python3 blinka_test.py
    Hello blinka!
    Digital IO ok!
    I2C ok!
    SPI ok!
    done!

Agora só falta escribir un script en Python para facer as lecturas do sensor, [semellante a este de Adafruit](https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/circuitpython-test). No meu caso tiven que indicar un enderezo de lectura do sensor (0x76) diferente ao que trae por defecto (0x77). Tomando ese código como referencia, fixen o script [BMP280_mqtt.py](sensors/BMP280_mqtt.py) para publicar as lecturas en MQTT, que colocaremos en `/home/pi/sensors/`, así como o servizo [bmp_mqtt.service](services/bmp_mqtt.service) que colocaremos en `/lib/systemd/system/` e que se encarga de iniciar o script en cada arranque da máquina.

Os datos son publicados nos _topic_ `casa/estudio2/temperatura` e  `casa/estudio2/presion` cada 5 minutos.

Resta calibrar o sensor de presión para que ofreza a presión relativa adecuada, e configuralo en modo `forced` para que non estea facendo miles de lecturas por minuto, o que consume enerxía innecesaria e ademais quenta o sensor.

### Activación do servizo
Unha vez que o arquivo `bmp_mqtt.service` está no cartafol `/lib/systemd/system/` temos que rexistrar o servizo en Systemd, comprobar o funcionamento e activar o inicio automático en cada inicio do sistema:

    # systemctl daemon-reload
    # systemctl start bmp_mqtt.service
    # systemctl status bmp_mqtt.service
    hdc_mqtt.service - HDC 1080 Pressure and Temperature Sensor Reading and MQTT Communication
    Loaded: loaded (/lib/systemd/system/hdc_mqtt.service; enabled; vendor preset: enabled)
    Active: active (running) since Sun 2020-11-15 10:11:03 GMT; 4h 4min ago
    Main PID: 24250 (python3)
    Tasks: 1 (limit: 2184)
    CGroup: /system.slice/hdc_mqtt.service
           └─24250 /usr/bin/python3 /home/pi/sensors/HDC1080_mqtt.py
    Nov 15 10:11:03 raspberry1 systemd[1]: Started HDV1080 Pressure and Temperature [...]
    # systemctl enable hdc_mqtt.service


