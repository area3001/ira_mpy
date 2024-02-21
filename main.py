import asyncio
import network
from ira import Ira

from machine import Pin
from neopixel import NeoPixel

pin = Pin(2, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 16)   # create NeoPixel driver on GPIO0 for 8 pixels
#np[0] = (255, 255, 255) # set the first pixel to white
#np.write()              # write data to all pixels


# nats publish -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'
def set_neopixel_rgb(data):
    color = data[2].lstrip('#')
    color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    np[int(data[1])] = (0, 0, 255)
    np.write()
    
    print('setting neopixel %d to %s' % (int(data[1]), color))

async def main():
    import network
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('area3001', 'hackerspace')
        while not sta_if.isconnected():
            pass
    
    print('network config:', sta_if.ifconfig())

    i = Ira('my_id', 'my_name', 'ira', '2024')
    i.register_handler('set_pixel', set_neopixel_rgb)
    
    await i.listen()
    print('listening to ira messages')

asyncio.run(main())