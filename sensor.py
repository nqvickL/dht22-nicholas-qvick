import dht
import machine
import time

sensor = dht.DHT22(machine.Pin(15))
led = machine.Pin("LED", machine.Pin.OUT)

while True:
    sensor.measure()
    temperature = sensor.temperature()
    if temperature > 25:
        led.on()
    else:
        led.off()
    print(temperature)
    time.sleep(2)
