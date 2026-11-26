# Nicholas Qvick
# INTKM26A2
# Harjoitus 4 MQTT ja lämpötila anturi DHT22

import dht
import machine
import time
from umqtt.simple import MQTTClient
import network

# Hotspot nimi
SSID = "Slop"

# Super turvallinen salasana
PASSWORD = "12345678"

# Komennot wlan moduulin aloittamiseksi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Printti verkkoon yhdistämiselle
print("Yhdistetään verkkoon...")

# Kun langatonta yhteyttä ei saada muodostettua lopettaa toiminnon
while not wlan.isconnected:
    time.sleep(1)

# ifconfig hakee verkon tiedot
ip = wlan.ifconfig()[0]
print("IP-osoite", ip)

# DHT22 sensori on pinnissä 22 (ohjeessa 15)
sensor = dht.DHT22(machine.Pin(21))
"""
led = machine.Pin("LED", machine.Pin.OUT)
"""

# Tämän hetkinen syöte "ei mitään"
cur_value = None

# MQTT osoite ja laitteen nimi
client = MQTTClient(
    b"picow",
    "iot.research.hamk.fi",
    # Katkaisee yhteyden minutin kuluttua
    keepalive=60
)
# Yhdistää MQTT
client.connect()


while True:
    # DHT22 anturi mittaa
    sensor.measure()
    # Tuple lämpötilalle ja kosteudelle
    new_data = (sensor.temperature(), sensor.humidity())
    # If jos data muuttuu ottaa lukeman
    if (cur_value != new_data):
        # vanha value ja uusi value
        cur_value = new_data
        # printtaa lämpötilan
        print(cur_value[0],"*C")
        # printtaa kosteuden
        print(cur_value[1], "%RH")
        # julkaisu mqtt palvelimelle
        client.publish(
            # Osoite lämpötilalle
            b"HAMK/Fo/DHT22/2604983/lampotila",
            # Encode muuttaa arvon biteiksi
            f'{cur_value[0]}'.encode()
        )
        client.publish(
            # Osoite kosteudelle
            b"HAMK/Fo/DHT22/2604983/kosteus",
            # Encode muuttaa arvon biteiksi
            f'{cur_value[1]}'.encode()
        )
    # Sensori lukee 10 sekunnin välein
    time.sleep(10)

# Katkaise yhteys
client.disconnect()