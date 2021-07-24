# MQTT e mosquitto

## Introducción

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

## Instalación e configuración de mosquitto

Os paquetes que instalan o servidor e os clientes en Ubuntu/Debian son

```
# apt install mosquitto mosquitto-clients
```

O servidor debería funcionar _out of the box_. Podemos probalo enviando e recibindo mensaxes:

+ Para que a nosa máquina se subscriba a unha canle basta con usar o cliente `mosquitto_sub`, indicandolle a IP do broker e o topic

      $ mosquitto_sub -h 192.168.0.5 -t proba/mensaxes

+ Para que a nosa máquina escriba unha mensaxe nunha canle basta con usar o cliente `mosquitto_pub`, indicandolle a IP do broker, o topic e o contido da mensaxe:

      $ mosquitto_pub -h 192.168.0.5 -t proba/mensaxes -m '“Mecajo no mundo'

## Funcionamento avanzado

Pode ser conveniente coñecer as `Clean Sessions` e as `Persistent Connections`, que xestionan como se conecta un cliente determinado a un broker, así como o tipo de envío que fai cada cliente:

+ `Clean Sessions`: (non persistente) o broker non almacena información sobre subscricións ou mensaxes sen enviar para o cliente. Ideal se o cliente só publica mensaxes. Non precisa `ClientID`.

+ `Persistent Connections`: (conexión estable ou duradeira) o broker pode almacenar mensaxes para o cliente por se este perde a conexión. Precisa dun `ClientID` único.

+ `Retained Messages`: no funcionamento por defecto, unha mensaxe publicada nun momento determinado só será entregada aos clientes que estean conectados nese preciso momento. Publicando a mensaxe coa opción `Retained Messages = TRUE` a última mensaxe recibida polo broker nun asunto sexa conservada por se un cliente se conecta posteriormente. É ideal se publicamos info de sensores ou estados de dispositivos, xa que así a información sempre estará dispoñible. O problema é que en principio non saberemos en que momento se publicou esta mensaxe.

## Clientes de mqtt

Existen varios clientes que nos poden resulta útiles para usar e analizar o que ocorre na nosa rede de comunicación:

+ [mqtt-explorer](http://mqtt-explorer.com/) (PC): este cliente gráfico permite observar todo o tráfico de mensaxes da nosa rede, visualizar a árbore de asuntos, facer gráficas con valores numéricos, revisar o historial, etc. Moi útil para investigar problemas. En linux pode instalarse fácilmente con :

      # snap install mqtt-explorer
+ [Mqtt Dashboard](https://play.google.com/store/apps/details?id=com.app.vetru.mqttdashboard&hl=en&gl=US) (Android): app para o móbil que permite enviar e recibir mensaxes MQTT mediante un panel con actuadores e cadros de control.

## Para saber máis

A información desta pequena guía esta sacada de :

+ [Introduction to IoT: Build an MQTT Server Using Raspberry Pi](https://appcodelabs.com/introduction-to-iot-build-an-mqtt-server-using-raspberry-pi) de _appcodelabs.com_.

+ [MQTT for Beginners: Tutorials and Course](http://www.steves-internet-guide.com/mqtt-basics-course/) de _steves-internet-guide.com_.

+ [Qué son y cómo usar los Topics en MQTT correctamente](https://www.luisllamas.es/que-son-y-como-usar-los-topics-en-mqtt-correctamente) de _luisllamas.es_.
