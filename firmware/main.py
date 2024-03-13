import asyncio
import network
from ira import Ira

from machine import Pin
from neopixel import NeoPixel

ssid = "area3001"
ssid_pwd = "hackerspace"

device_id = "0001"
device_name = "Badge Daan"
device_hardware = "area3001_badge"
device_version = "2024.1"

pixel_count = 26
pin = Pin(2, Pin.OUT)
np = NeoPixel(pin, pixel_count)


# nats publish -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'
async def set_neopixel_rgb(data):
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


async def clear_neopixel_rgb(data):
    for i in range(pixel_count - 1):
        np[i] = (0, 0, 0)
        
    np.write()
    print('clearing all neopixels')


def main():
    import network
    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        #sta_if.config(hidden=True)
        sta_if.connect(ssid, ssid_pwd)
        while not sta_if.isconnected():
            pass

    print('network config:', sta_if.ifconfig())

    i = Ira(device_id, device_name, device_hardware, device_version)
    i.register_handler('set_pixel', set_neopixel_rgb)
    i.register_handler('clear_pixels', clear_neopixel_rgb)

    asyncio.run(i.listen())
    print('listening to ira messages')

    asyncio.get_event_loop().run_forever()

main()