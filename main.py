import config
import asyncio
import network
import time
from ira import Ira

from machine import Pin
from neopixel import NeoPixel

pin = Pin(config.pinOutNumber, Pin.OUT)
np = NeoPixel(pin, config.pixel_count)

# nats publish -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'
async def set_neopixel_rgb(data):
    #print(data)
    
    #check for valid data like this ['set_pixel', '0 #00ff00']
    if len(data) != 2:
        print('No command arguments')
        return
    
    pairs = data[1].split(',')
    for p in pairs:
        addr_color = p.split()
        if len(addr_color) != 2:
            print('Invalid argument pairs {}' % p)
            return
        
        color = addr_color[1].lstrip('#')
        color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        #print('Hex to RGB: ',addr_color[1], ' -> ', color)
        addr = int(addr_color[0]) % config.pixel_count      
        np[addr] = color

    np.write()


async def clear_neopixel_rgb(data):
    print('Clearing all neopixels!')
    for i in range(config.pixel_count - 1):
        np[i] = (0, 0, 0)
        
    np.write()
    

def main():
    print("""
     ___ ____      _    
    |_ _|  _ \    / \   
     | || |_) |  / _ \  
     | ||  _ <  / ___ \ 
    |___|_| \_\/_/   \_\

    """)
    print('Boot up IRA version: {}'.format(config.device_version))
    print('Deviceid:', config.device_id)
    print('Device Name:', config.device_name, )
    print('Hardware:', config.device_hardware)
    
    print('Pinout number:', config.pinOutNumber)
    print('Leds count:', config.pixel_count)
    
    #ACTIVATE WIFI, CONNECT TO ROUTER
    wlan = network.WLAN(network.STA_IF) #Stands for Station Interface
    
    connection_timeout = 10  # Timeout in seconden
    start_time = time.time()

    if wlan.isconnected():
        print('We are already in connected state with wifi.')
    else:
        print('We are not connected to network...')
        wlan.active(False)
        wlan.active(True)
        #sta_if.config(hidden=True) #@Hackerspace the wifi is hidden.
        print("Connecting to router...")
        wlan.connect(config.wifi_ssid, config.wifi_password)
        
        #CHECK IF CONNECTED TO WLAN
        while not wlan.isconnected():
            if time.time() - start_time > connection_timeout:
                print("Failed to connect within the timeout period. Please check your Wifi credentials.")
            break  # Verlaat de lus als we de timeout hebben bereikt
            #pass# LOOP UNTIL CONNECTED
    
    if wlan.isconnected():
        print("Retrieving Network Configuration from: [", config.wifi_ssid, "].")
        print('Network config:', wlan.ifconfig())
    else:
        print("Not connected to WiFi. Please check your SSID and password.")

    #Send clear event when we do soft reboot, (leds can still be lighting up)
    clear_neopixel_rgb(None)

    i = Ira(config.device_id, config.device_name, config.device_hardware, config.device_version)
    i.register_handler('set_pixel', set_neopixel_rgb)
    i.register_handler('clear_pixels', clear_neopixel_rgb)

    asyncio.run(i.listen())
    print('Listening to ira messages')

    asyncio.get_event_loop().run_forever()

main()