# Conectar un sensor CCS811 na Raspberry PI

Esta guía está baseada en [Adafruit CCS811 Air Quality Sensor](https://learn.adafruit.com/adafruit-ccs811-air-quality-sensor/python-circuitpython) e [Adafruit CircuitPython CCS811 Library](https://github.com/adafruit/Adafruit_CircuitPython_CCS811)

## Conexión á Raspberry, NodeMCU ou Arduino
### Cableado
Hai 4 cables que unen o sensor CCS811 co porto I2C. Dous son para a alimentación e outros dous para a transmisión de datos. Resulta bastante práctico para isto usar cable telefónico de 4 fios, que se pode estender varios metros sen problema, aínda que as unións son un pouco fráxiles:
Módulo HDC1080 | Raspberry Pi | Node MCU | Arduino | Función
------------ | -------------| -------------| -------------| -------------
3v3/5v (Vermello)  | 3v3 | 3v3| 3v3 | Alimentación
GND (Negro) | GND | GND | GND |Terra
S __D__ A (Verde) | SDA – Pin 3  | SDA – D2 | SDA – A4 | Datos ( __D__ ata)
S __C__ L (Amarelo) | SCL – Pin 5 | SCL – D1 | SCL – A5 | Reloxo (__C__ lock)

### Software 
É necesario instalar e activar diversas dependencias para traballar co BUS i2c, tal como se explica no [*howto* para o sensor BMP](documentacion/bmp280_howto.md).

Ademáis teremos que instalar a librería adafruit-circuitpython-ccs811
 Resumindo, as ordes son:

    # apt update                <-- sincroniza a lista de software dispoñible
    # apt full-upgrade          <-- executa todas as actualizacións posibles
    # apt-get install -y python-smbus i2c-tools
    # raspi-config              <-- acceder á opción 5 Interfacing Options e activar i2c
    $ ls /dev/i2c* /dev/spi*	<--comprobar que o bus i2c é accesible
    $ i2cdetect -y 1			<--comprobar que o sensor está no enderezo 0x40
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: -- -- -- -- -- -- -- -- -- -- 5a -- -- -- -- --
    # pip3 install RPI.GPIO
    # pip3 install adafruit-circuitpython-busdevice adafruit-circuitpython-ccs811

Pódese probar se o sensor está funcionando ben con este test extraido do README da librería 

    $ pi@raspberry1:~/tests $ python3 CCS811_test.py
    CO2: 0 PPM, TVOC: 0 PPB
    CO2: 400 PPM, TVOC: 0 PPB
    CO2: 439 PPM, TVOC: 5 PPB
    CO2: 536 PPM, TVOC: 20 PPB
    CO2: 486 PPM, TVOC: 13 PPB

O incremento nas cifras é o resultado de espirar sobre o sensor.
    
Tomando ese código como referencia, fixen o script [CCS811_mqtt.py](sensors/CCS811_mqtt.py) para publicar as lecturas en MQTT, que colocaremos en `/home/pi/sensors/`, así como o servizo [ccs_mqtt.service](services/hdc_mqtt.service) que colocaremos en `/lib/systemd/system/` e que se encarga de iniciar o script en cada arranque da máquina.
Os datos son publicados nos _topic_ `casa/estudio/eco2` e `casa/estudio/tvoc` cada 5 minutos.

### Activación do servizo
Rexistramos o servizo en Systemd, comprobamos o funcionamento e activamos o inicio automático. Convén reiniciar a máquina con `# reboot` e comprobar se temos lecturas do sensor no broker mqtt usando, por exemplo, o MQTT Explorer no PC.
