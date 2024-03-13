import asyncio
import network
from ira import Ira

from machine import Pin
from neopixel import NeoPixel

ssid = "area3001"
ssid_pwd = "hackerspace"

device_id = "0002"
device_name = "IRA von Kris"
device_hardware = "IRA115"
device_version = "2024.1"

pixel_count = 30
pixel_count = 30
pin = Pin(2, Pin.OUT)
np = NeoPixel(pin, pixel_count)

# For MAC
# nats publish -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'

# For Windows (Go) command
# nats-pub -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'
# nats-pub -s nats://demo.nats.io:4222 area3001.ira.default.output 'clear_pixels'

def set_neopixel_rgb(data):
    #print(data)
    
    if len(data) != 2:
        print('no command arguments')
        return
    
    pairs = data[1].split(',')
    for p in pairs:
        addr_color = p.split()
        if len(addr_color) != 2:
            print('invalid argument pairs {}' % p)
            return
        
        color = addr_color[1].lstrip('#')
        color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        addr = int(addr_color[0]) % pixel_count
        
        np[addr] = color

    np.write()
    
def clear_neopixel_rgb(data):
    for i in range(pixel_count - 1):
        np[i] = (0, 0, 0)
        
    np.write()
    print('clearing all neopixels')


async def main():
    print('Boot up IRA version: {}'.format(device_version))
    #ACTIVATE WIFI, CONNECT TO ROUTER
    wlan = network.WLAN(network.STA_IF) #Stands for Station Interface
    
    if wlan.isconnected():
        print('We are already in connected state')
    else:
        print('We are not connected to network...')
        wlan.active(False)
        wlan.active(True)
        #sta_if.config(hidden=True) #@Hackerspace the wifi is hidden.
        print("Connecting to router...")
        wlan.connect(ssid, ssid_pwd)
        
        #CHECK IF CONNECTED TO WLAN
        while not wlan.isconnected():
            pass# LOOP UNTIL CONNECTED
    
    print("Retrieving Network Configuration")
    print('network config:', wlan.ifconfig())

    i = Ira(device_id, device_name, device_hardware, device_version)
    i.register_handler('set_pixel', set_neopixel_rgb)
    i.register_handler('clear_pixels', clear_neopixel_rgb)

    await i.listen()
    print('Listening to ira messages')
        
asyncio.run(main())