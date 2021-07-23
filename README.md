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

Se precisas unha axuda máis detallada para comezar coa Raspberry e con GNU/Linux, podes consultar o [titorial de Francisco Moya](https://franciscomoya.gitbooks.io/taller-de-raspberry-pi/content/es/)

### Instalación e arranque

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

## Configuración tras o primeiro inicio
Para traballar con
Debemos levar a cabo os seguintes pasos tras un primeiro inicio de sesión exitoso:

1. Cambiar o contrasinal por defecto con
 `$ passwd`
2. Executar `raspi-config` e axustar o seguinte:

  + `3 Interface Options --> P5 Enable I2C`. Isto usaremolo máis adiante para conectar sensores.

  + `6 Advanced Options --> A1 Expand Filesystem`. O tamaño da partición de sistema creada na instalación é moi pequena e nin sequera se pode actualizar o SO.

  + En caso de que estea sen facer, activar o acceso mediante SSH e configurar a rede.

3. Actualizar o sistema:
```
# apt-get update
# apt-get upgrade
```

4. Instalar algúns programas útiles para traballar coa Rapsberry PI:
  + `mc` é un explorador de arquivos para consola que nos permite manipular fácilmente arquivos e cartafoles incluso entre dispositivos da nosa rede.
  + `screenfetch` ofrece información básica sobre o hardware e o SO.  
```
# apt install mc screenfetch
```

## Configuración para IoT

Debemos instalar e configurar o sistema de comunicacións MQTT, a base de datos InfluxDB e o servidor de gráficos Grafana.

### MQTT e `mosquitto`

MQTT é un protocolo de comunicación simple sobre TCP/IP que encaixa perfectamente no contexto de IoT. Os clientes MQTT intercambian mensaxes, que son pequenos anacos de texto plano máis ou menos estructurado. Usaremos este sistema para transmitir información entre sensores e actuadores.

Esta guia traballa coa versión 3 do protocolo MQTT. Recentemente foi publicada a versión 5, que mellora substancialmente algunhas características pero (por falta de tempo) de momento non podemos adoptar.

A terminoloxía e funcionamento básico do protocolo MQTT é:
+ `broker` e o servidor intermediario que xestiona a entrada e saída de mensaxes. Pode funcionar nun PC ou Raspberry. O  broker mais popular é `mosquitto`, que é software libre.

+ Os dispositivos emisores (publishers) e receptor (subscribers) son os dous tipos de clientes, puidendo actuar un dispositivo como emisor e receptor simultáneamente.

+ As canles de comunicación (ou asuntos) chámanse `topics` e teñen a forma de etiquetas aniñadas en árbore, como `horta/sensor/temperatura1` ou `casa/andar0/salon/lampara1`.

+ Cando se describen canles para subscripcións, o comodín `+` substitúe a un só nivel de asuntos e o comodín `#` substitúe a todos os niveis inferiores. Isto permite que un cliente estea subscrito a varias canles ou asuntos simultáneamente:  `horta/sensor/#`

+ Un cliente pode escoitar todas as canles nas que estea subscrito, por exemplo:
  + `horta/sensor/#/` escoitará todas as mensaxes de todas as canles que colgan de __horta/sensor__.

  + `casa/andar0/salon/lampara/1/#` escoitará todas as mensaxes da lámpara 1.


+ Un emisor pode enviar mensaxes a calquera das canles. Esta mensaxe recíbea o broker, que verifica os permisos do emisor para esas canles e en caso afirmativo reenvía a mensaxe aos subscriptores.

A información desta pequena guía esta sacada de :

+ [Introduction to IoT: Build an MQTT Server Using Raspberry Pi](https://appcodelabs.com/introduction-to-iot-build-an-mqtt-server-using-raspberry-pi) de _appcodelabs.com_.

+ [MQTT for Beginners: Tutorials and Course](http://www.steves-internet-guide.com/mqtt-basics-course/) de _steves-internet-guide.com_.

+ [Qué son y cómo usar los Topics en MQTT correctamente](https://www.luisllamas.es/que-son-y-como-usar-los-topics-en-mqtt-correctamente) de _luisllamas.es_.

### Instalación e configuración de mosquitto

Os paquetes que instalan o servidor e os clientes en Ubuntu/Debian son

```
# apt install mosquitto mosquitto-clients
```

O servidor debería funcionar _out of the box_. Podemos probalo enviando e recibindo mensaxes:

+ Para que a nosa máquina se subscriba a unha canle basta con usar o cliente `mosquitto_sub`, indicandolle a IP do broker e o topic

      $ mosquitto_sub -h 192.168.0.25 -t "proba/mensaxes"

+ Para que a nosa máquina escriba unha mensaxe nunha canle basta con usar o cliente `mosquitto_pub`, indicandolle a IP do broker, o topic e o contido da mensaxe:

      $ mosquitto_pub -h 192.168.0.25 -t "proba/mensaxes" -m “Mecajonomundo”

### Funcionamento avanzado

Pode ser conveniente coñecer as `Clean Sessions` e as `Persistent Connections`, que xestionan como se conecta un cliente determinado a un broker, así como o tipo de envío que fai cada cliente:

+ `Clean Sessions`: (non persistente) o broker non almacena información sobre subscricións ou mensaxes sen enviar para o cliente. Ideal se o cliente só publica mensaxes. Non precisa `ClientID`.

+ `Persistent Connections`: (conexión estable ou duradeira) o broker pode almacenar mensaxes para o cliente por se este perde a conexión. Precisa dun `ClientID` único.

+ `Retained Messages`: no funcionamento por defecto, unha mensaxe publicada nun momento determinado só será entregada aos clientes que estean conectados nese preciso momento. Publicando a mensaxe coa opción `Retained Messages = TRUE` a última mensaxe recibida polo broker nun asunto sexa conservada por se un cliente se conecta posteriormente. É ideal se publicamos info de sensores ou estados de dispositivos, xa que así a información sempre estará dispoñible. O problema é que en principio non saberemos en que momento se publicou esta mensaxe.


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
- [ ] Habilitar o acceso por SSH mediante claves asimétricas.
- [ ] Automatizar unha copia de seguridade da base de datos noutro dispositivo diferente.
- [ ] Crear arquivo de configuración para centralizar as variables usadas nos scripts, como enderezos IP, topics, acceso Wifi, etc.
- [ ] Substituir o script `influxdb_mqtt.service` por outro con licencia libre.
- [ ] Publicar os datos dos sensores en formato JSON.
- [ ] Habilitar acceso seguro desde o exterior aos datos.

## Hardware

- [ ] Adaptación dunha protoboard para conectar os diferentes sensores aos terminais I2C do GPIO

![Raspberry PI, escudo e sensores](documentacion/imaxes/raspberry-shield-and-sensors.jpg)

### Por facer (TO-DO)

- [ ] Incluir a comunicación por LORA Monocanle
