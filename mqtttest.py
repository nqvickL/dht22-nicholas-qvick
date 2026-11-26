from umqtt.simple import MQTTClient
import network
import time

# Hotspot nimi
SSID = "Slop"

# Super turvallinen salasana
PASSWORD = "12345678"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Yhdistetään verkkoon...")

while not wlan.isconnected:
    time.sleep(1)

ip = wlan.ifconfig()[0]
print("IP-osoite", ip)
client = MQTTClient(
    b"picow",
    "iot.research.hamk.fi",
    keepalive=60
)
client.connect()

client.publish(
    b"HAMK/Fo/testi",
    b"hei"
)
client.disconnect()