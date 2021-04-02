<h1>IoT server over RaspberryPi (for interior use)</h1>
<p>Podes ler tamén a <a href="README.md">versión orixinal en galego</a> deste arquivo</p>
<h2>Software</h2>
<p>IOT server configuration and setup over RaspberyPi. Offers different services for a basic IoT server:
<ul>
  <li>Base Operating System: Raspberry Pi OS Lite</li>
  <li>MQTT Message Server (Broker): mosquitto</li>
  <li>IoT Database: InfluxDB</li>
  <li>Data Graphical Server: Grafana</li>
  <li>Python scripts to read data from a few sensors:</li>
  <ul>
    <li>Temperature and atmosferical pressure: BMP280</li>
    <li>Temperature and relative huumidity: HDC1080</li>
    <li>Air quality: CCS-811</li>
  </ul>
    <li>Python script to extract data from MQTT messages and write them in the InfluxDB database</li>
    <li>SystemD scripts to start on boot the previous scripts as services</li>
</ul>
</p>
<p>To do
  <ul>
    <li>Order tis files and scripts in a simple and coherent way</li>
    <li>Create a config file to host local variables like IP adsresses, topics, Wifi passwords, etc.</li>
    <li>Add secure access from internet to the IoT data</li>
    <li>Publish the sensors data in JSON format</li>
  </ul>
</p>
<h2>Hardware</h2>
<ul>
  <li>DIY shield to easy connect the different sensors to the GPIO I2C terminals</li>
  </ul>
<p>To do
  <ul>
    <li>Include monochannel LORA comunication</li>
  </ul>
</p>
