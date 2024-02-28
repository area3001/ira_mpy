import asyncio
import network
from ira import Ira

from machine import Pin
from neopixel import NeoPixel

pixel_count = 26
pin = Pin(2, Pin.OUT)
np = NeoPixel(pin, pixel_count)


# nats publish -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'
def set_neopixel_rgb(data):
    print(data)
    
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
        np[int(addr_color[0])] = color
        print('setting neopixel %d to %s' % (int(addr_color[0]), color))

    np.write()
    
def clear_neopixel_rgb(data):
    for i in range(pixel_count - 1):
        np[i] = (0, 0, 0)
        
    np.write()
    print('clearing all neopixels')


async def main():
    import network
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.config(hidden=True)
        sta_if.connect('area3001_iot', 'hackerspace')
        while not sta_if.isconnected():
            pass
    
    print('network config:', sta_if.ifconfig())

    i = Ira('my_id', 'my_name', 'ira', '2024')
    i.register_handler('set_pixel', set_neopixel_rgb)
    i.register_handler('clear_pixels', clear_neopixel_rgb)
    
    await i.listen()
    print('listening to ira messages')

asyncio.run(main())