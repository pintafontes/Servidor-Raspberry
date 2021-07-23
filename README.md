# Servidor para IoT sobre RaspberryPi (para uso en interiores)
NOTE: In the near future there will be an [english version of this documentation](README_en.md)

Con este proxecto conseguimos usar unha Rasperry Pi 2 ou superior como unha _centralita_ de dispositivos IoT. Ademais conectaremos ao seu porto GPIO un ou máis sensores que nos aportarán datos do lugar onde esta instalada a Raspi.

![Raspberry PI, sensores e Grafana](documentacion/imaxes/raspberry-sensors-and-grafana.jpg)

## Software
Configuración e posta a punto do servidor IoT sobre RaspberyPi. Ofrece diferentes servizos para un sistema de IoT básico:

* Sistema Operativo de base: [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/)
* Servidor de mensaxería MQTT: [Mosquitto](https://mosquitto.org/)
* Servidor de base de datos IoT: [InfluxDB](https://www.influxdata.com/products/influxdb/)
* Servidor de gráficos de datos: [Grafana](https://grafana.com/)

## Configuración de Raspberry Pi OS
Existen a posibilidade de realizar as seguintes operacións para configurar a Raspberry accedendo en modo gráfico ou cunha pantalla HDMI. Aquí explico o método _headless_, que non precisa pantalla nin teclado.
1. Instalamos a ISO correspondente na tarxeta SD ou __pendrive (*)__ correspondente. Escribiranse dúas particións no dispositivo:
  - `BOOT` de tipo FAT32, coa configuración básica de arranque.
  - `ROOTFS` con toda a estructura de arquivos e cartafois do SO.
2. Sen retirar a SD/USB do noso PC, activamos o acceso por SSH creando un arquivo baleiro `ssh.txt` na partición `BOOT`.
3. Debemos usar unha IP fixa para poder comunicarnos co servidor. Ademáis, é preferible usar conexión de cable LAN, que é máis fiable e menos propensa a fallos; pero tampouco debería haber problemas en usar unha rede Wifi. Modificamos o arquivo `/etc/dhcpcd.conf` (na partición `ROOTFS`) para configurar os parámetros da rede, comentando ou descomentando as liñas referentes á interface que vaiamos usar (`eth0` para LAN e `wlan0` para wifi).
```
# Exemplo de IP estática para LAN:
interface eth0
static ip_address=192.168.1.25/24
static routers=192.168.1.1
# DNS de Google
# static domain_name_servers=8.8.8.8 8.8.4.4
# DNS de R
static domain_name_servers=213.60.205.175
# Exemplo de IP estática para WIFI:
interface wlan0
static ip_address=192.168.1.25/24
static routers=192.168.1.1
# DNS de Google
static domain_name_servers=8.8.8.8 8.8.4.4
# DNS de R
static domain_name_servers=213.60.205.175
```

4. Se usamos unha rede Wifi, tamén haberá que incluir as credenciais de acceso á mesma no arquivo `/etc/wpa_supplicant/wpa_supplicant.conf`:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=ES
network={
	ssid="NOME_da_WIFI"
	psk="CONTRASINAL"
}
```
##### (*) BONUS

É case imprescindible que o SO se instale sobre un pendrive e se execute desde o mesmo para mellorar o rendemento e a fiabilidade. A lectura e escritura de arquivos é máis rápida no pendrive e ademáis as tarxetas SD soen estropearse cando levan un tempo executando un SO, pois non aguantan ben o ritmo de lecura e escritura propio deste uso.

Dependendo do modelo de RPi que estamos usando, o arranque por USB pode ser directo (modelo `RPi 2B 1.2` en diante) ou iniciado por unha SD (modelo `RPi 2B 1.1` e anteriores). Podemos determinar o modelo executando:
```
# cat /proc/device-tree/model
Raspberry Pi 2 Model B Rev 1.1
```
ou de forma mais vistosa coa ferramenta `pinout`, que representa a placa da RPi coas súas entradas e saídas

+ [Instruccións usando o arquivo bootcode.bin](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/README.md). Vale para a maioría dos modelos de RPi.
+ [Instruccións en atareao.es](https://atareao.es/tutorial/raspberry-pi-primeros-pasos/volando-con-la-raspberry-desde-usb/). Vale para os modelos máis novos de RPi.
+ [Instruccións en raspberrypi.org](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md). Vale para os modelos máis novos de RPi.

## Scripts en Python
* Scripts en Python que __leen os datos__ dos diferentes sensores. Estes datos son publicados como mensaxes MQTT.
* Scripts de `Systemd` que inician *automáxicamente* os anteriores scripts como **servizos**.

| Magnitude | Sensor | Script de lectura (/sensors) | Servizo (/services) | Documentación |
|---| --- | --- | --- | --- |
| Temperatura e Presión Atmosférica | BMP280 | BMP280_mqtt.py | bmp_mqtt.service | [BMP280 HowTo](documentacion/bmp280_howto.md) |
| Temperatura e Humidade Relativa | HDC1080 | HDC1080_mqtt.py | hdc_mqtt.service | [HDC1080 HowTo](documentacion/hdc1080_howto.md) |
| Calidade do aire | CCS-811 | CCS811_mqtt.py | ccs_mqtt.service |  |
| Temperatura e Humidade Relativa | DHT22 | ─ | ─ | Non recomendado

* Utilización do script-Python de [diyi0t.com](https://diyi0t.com/visualize-mqtt-data-with-influxdb-and-grafana/) que extrae os datos de certas mensaxes MQTT e os escribe na base de datos InfluxDB: [influxdb_mqtt.service](services/influxdb_mqtt.service). Lamentablemente, este script non é software libre e debemos atopar outra maneira de escribir os datos MQTT en InfluxDB
### Por facer (TO-DO)

- [x] Ordenar os arquivos e scripts de forma coherente e sinxela.
- [ ] Automatizar unha copia de seguridade da base de datos noutro dispositivo diferente.
- [ ] Crear arquivo de configuración para centralizar variables como enderezos IP, topics, acceso Wifi, etc.
- [ ] Substituir o script `influxdb_mqtt.service` por outro con licencia libre.
- [ ] Publicar os datos dos sensores en formato JSON.
- [ ] Habilitar acceso seguro desde o exterior aos datos.

## Hardware

* Adaptación dunha protoboard para conectar os diferentes sensores aos terminais I2C do GPIO

![Raspberry PI, escudo e sensores](documentacion/imaxes/raspberry-shield-and-sensors.jpg)

### Por facer (TO-DO)

- [ ] Incluir a comunicación por LORA Monocanle
