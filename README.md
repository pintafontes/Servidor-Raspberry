<h1>Servidor para IoT sobre RaspberryPi (para uso en interiores)</h1>
<p>You can also read this file in the <a href="README_en.md">english version</a></p>
<h2>Software</h2>
<p>Configuración e posta a punto do servidor IoT sobre RaspberyPi. Ofrece diferentes servizos para un sistema de IoT básico:
<ul>
  <li>Sistema Operativo de base: Raspberry Pi OS Lite</li>
  <li>Servidor de mensaxería MQTT: mosquitto</li>
  <li>Servidor de base de datos IoT: InfluxDB</li>
  <li>Servidor de gráficos de datos: Grafana</li>
  <li>Scripts en Python para a lectura de varios sensores:</li>
  <ul>
    <li>Presión atmosférica e temperatura: BMP280</li>
    <li>Temperatura e humidade ambiental: HDC1080</li>
    <li>Calidade do aire: CCS-811</li>
  </ul>
    <li>Script en Python que extrae os datos de certas mensaxes MQTT e os escribe na base de datos InfluxDB</li>
    <li>Scripts de SystemD que inician automáxicamente os anteriores scripts como servizos</li>
</ul>
</p>
<p>Por facer (TO-DO)
  <ul>
    <li>Ordenar os arquivos e scripts de forma coherente e sinxela</li>
    <li>Crear arquivo de configuración para centralizar variables como enderezos IP, topics, acceso Wifi, etc.</li>
    <li>Habilitar acceso seguro desde o exterior aos datos</li>
    <li>Publicar os datos dos sensores en formato JSON</li>
  </ul>
</p>
<h2>Hardware</h2>
<ul>
  <li>Deseño dunha placa-escudo para conectar os diferentes sensores aos terminais I2C do GPIO</li>
  </ul>
<p>Por facer (TO-DO)
  <ul>
    <li>Incluir a comunicación por LORA Monocanle</li>
  </ul>
</p>
