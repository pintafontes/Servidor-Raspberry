# Instalar un servidor (broker) de MQTT (mosquitto) na Raspberry PI

Baseado en https://appcodelabs.com/introduction-to-iot-build-an-mqtt-server-using-raspberry-pi

MQTT é un protocolo de comunicación simple sobre TCP/IP, moi semellante ás canles de Telegram, que encaixa perfectamente no contexto de IoT. Sorprende a eficacia e fiabilidade do seu funcionamento, aínda que a súa sinxeleza tamén conleva algunhas limitacións coas que teremos que lidiar.

A terminoloxía e funcionamento básico é:

* `broker`: e o servidor intermediario que xestiona a entrada e saída de mensaxes. Pode funcionar nunha Raspberry, nun PC ou tamén se poden usar servizos da nube. O broker mais popular é [mosquitto](https://mosquitto.org/), que é software libre.

* Hai dous tipos de __clientes__ que se conectan ao broker: os dispositivos que emiten mensaxes (_publishers_) e os que reciben mensaxes (_subscribers_) , puidendo ser o mesmo dispositivo.

* As canles de comunicación ou __asuntos__ chámanse `topics` e teñen a forma de etiquetas aniñadas en árbore, como `horta/bancal1/temperatura` ou `casa/andar0/salon/lampara1`. Máis información sobre topics [no blogue de Luis Llamas](https://www.luisllamas.es/que-son-y-como-usar-los-topics-en-mqtt-correctamente)

* Un cliente pode subscribirse simultáneamente a tantas canles como sexa necesario. Hai comodíns que permiten a un cliente escoitar varios asuntos :
  * "__+__" substitúe a un só nivel. Subscribindo un dispositivo a `horta/+/temperatura` estaríamos recibindo todas as mensaxes sobre temperatura da horta, supoñendo que haxa diferentes sensores en diferentes lugares.
  * "__#__" substitúe a todos os niveis inferiores. Subscribindonos a `horta/bancal1/#` estaríamos recibindo todas as magnitudes que se midan no bancal 1 da horta.
* En principio un emisor pode enviar mensaxes a calquera das canles. Esta mensaxe recíbea o broker, que verifica os permisos do emisor para esas canles e en caso afirmativo reenvía a mensaxe aos subscriptores.
* As mensaxes son pequenos anacos de texto que intercambia información entre os sensores e os actuadores. Poden enviarse en texto plano, aínda que o máis usado actualmente é o formato JSON.

## Instalación, configuración e comprobación de funcionamento
Os paquetes que instalan o servidor e os clientes en Ubuntu/Debian son 
    
    # apt install mosquitto mosquitto-clients

Para que a nosa máquina se subscriba a unha canle basta con usar o cliente `mosquitto_sub`, indicandolle a IP do broker (-h) e o topic (-t)
    
    $ mosquitto_sub -h 192.168.0.25 -t "proba/mensaxes"

Para que a nosa máquina escriba unha mensaxe nunha canle basta con usar o cliente `mosquitto_pub`, indicandolle a IP do broker (-h), o topic (-t) e o contido da mensaxe (-m):

    $ mosquitto_pub -h 192.168.0.25 -t "proba/mensaxes" -m “MeCajoNoMundo”

## Funcionamento avanzado

Tomado de http://www.steves-internet-guide.com/mqtt-basics-course/

* Clean Sessions e Persistent Connections: cando o cliente se conecta a un broker pode usar unha conexión persistente ou non persistente:
  * __Clean Sessions__: (non persistente) o broker non almacena información sobre subscricións ou mensaxes sen enviar para o cliente. Ideal se o cliente só publica mensaxes. Non precisa ClientID
  * __Persistent Connections__: (conexión estable ou duradeira) o broker pode almacenar mensaxes para o cliente por se este perde a conexión. Precisa ClientID único.
* __Retained Messages__: no funcionamento por defecto unha mensaxe publicada nun momento determinado só será entregada aos clientes que estean conectados nese mesmo momento. Con esta opción activada, a última mensaxe recibida polo broker nun asunto sexa conservada por se un cliente se conecta posteriormente. É ideal se publicamos info de sensores ou estados de dispositivos, xa que así a última información sempre estará dispoñible.

## Usar un cliente de MQTT en Python3

Baseado en http://www.steves-internet-guide.com/into-mqtt-python-client/

A librería `paho_mqtt` permite publicar mensaxes nunha rede MQTT con información dispoñible dentro dun script Python. É necesario instalar o paquete de Python

    # pip3 install paho-mqtt

Úsase a librería paho.mqtt (`import paho.mqtt.client as mqtt`), que precisa como mínimo os seguintes parámetros para funcionar. Estes parámetros gardámolas en variables ao comezo do código para que sexa algo sinxelo cambialas se fora necesario:

* o enderezo IP da máquina onde está o servidor broker de MQTT: broker_IP="192.168.0.25"
* o nome que se lle dá a este cliente (útil para saber no servidor quen se conecta ou quen publica as mensaxes): `client = mqtt.Client("RaspiDHT")`
* Establécese unha conexión para cada publicación (que se interrompe en poucos segundos): `client.connect(broker_IP)`
* Publicamos a mensaxe no topic escollido: `client.publish("horta/bancal1/temperatura","Temp = {0:0.1f}ºC".format(temperature))`

Con esta configuración, un cliente que se conecte ao broker terá que esperar a que se publique un dato (cada 5 min) para recibir información. Para cambiar este comportamento, podemos publicar a mensaxe coa opción retain = True, polo que o servidor gardará sempre a última mensaxe disponible e será o que reciba o cliente cando se conecte:

`client.publish("/andar1/sensor/1/", "Temp = {0:0.1f}ºC".format(temperature), qos=0,retain=True)`

A opción `qos=0` implica que as mensaxes envíanse sen acuse de recibo, o que permite que o servidor non teña que estar pendente de se os clientes enstán activos ou non.
