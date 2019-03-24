import os
from collections import deque
from pathlib import Path
from time import sleep
from gpiozero import LED
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from tinydb import TinyDB, Query

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Configure GPIO
valve = LED(19)

# Configure database
home_dir = str(Path.home())
db = TinyDB(os.path.join(home_dir, 'config_db.json'))
config_db = db.table('config', cache_size=0)
Key = Query()
on_threshold = config_db.search(Key.key == 'water_on_threshold')[0]['value']
off_threshold = config_db.search(Key.key == 'water_off_threshold')[0]['value']

queue = deque([], 10)
loopcount = 0
while True:
    loopcount += 1
    if loopcount % 10 == 0:
        on_threshold = config_db.search(Key.key == 'water_on_threshold')[0]['value']
        off_threshold = config_db.search(Key.key == 'water_off_threshold')[0]['value']
        print('on:{} off:{}'.format(on_threshold, off_threshold))
        print('rs:{}'.format(queue))

    currentreading = mcp.read_adc(0)
    queue.append(currentreading)
    config_db.upsert({
        'key': 'current_moisture_value',
        'value': currentreading
    }, Key.key == 'current_moisture_value')
    if not valve.is_lit and all([x < on_threshold for x in queue]):
        valve.on()
        config_db.upsert({
            'key': 'water_state',
            'value': True
        }, Key.key == 'water_state')
        print('turn water on')
    if valve.is_lit and all([x > off_threshold for x in queue][-3:]):
        valve.off()
        config_db.upsert({
            'key': 'water_state',
            'value': False
        }, Key.key == 'water_state')
        print('turn water off')
    sleep(0.1)
