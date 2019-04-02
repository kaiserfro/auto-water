import os
from collections import deque
from time import sleep
from gpiozero import LED
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import requests

url = 'https://water-inator.appspot.com'

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Configure GPIO
valve = LED(19)

def get_on_threshold():
    r = requests.get('{}/get_on_threshold'.format(url))
    if r.status_code == 200:
        return r.json()['value']
    return 350

def get_off_threshold():
    r = requests.get('{}/get_off_threshold'.format(url))
    if r.status_code == 200:
        return r.json()['value']
    return 600

def send_current_reading(value):
    r = requests.get('{}/set_current_moisture_value/{}'.format(url, value))
    return r.status_code

def send_water_state(value):
    r = requests.get('{}/set_water_state/{}'.format(url, 'true' if value else 'false'))
    return r.status_code

# Configure database
on_threshold = get_on_threshold()
off_threshold = get_off_threshold()

queue = deque([], 10)
loopcount = 0
while True:
    currentreading = mcp.read_adc(0)

    loopcount += 1
    if loopcount % 10 == 0:
        on_threshold = get_on_threshold()
        off_threshold = get_off_threshold()
        print('on:{} off:{}'.format(on_threshold, off_threshold))
        print('rs:{}'.format(queue))
        send_current_reading(currentreading)

    queue.append(currentreading)
    if not valve.is_lit and all([x < on_threshold for x in queue]):
        valve.on()
        send_water_state(True)
        print('turn water on')
    if valve.is_lit and all([x > off_threshold for x in queue][-3:]):
        valve.off()
        send_water_state(False)
        print('turn water off')
    sleep(0.1)
