import config
import asyncio
import network
import time
import sys
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
        
        color = addr_color[1].lstrip('#') # we vragen hex kleur op.
        color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4)) # we zetten hex om naar RGB
        print('Hex to RGB: ',addr_color[1], ' -> ', color) #weergeven wat hex als RGB waarde heeft.
        
        if int(addr_color[0]) < config.pixel_count:
            addr = int(addr_color[0]) #% config.pixel_count #We maken adres positie aan indien het binnen de pixelcount range zit.
            print("Adres:", int(addr_color[0]), "Set:", color)
            np[addr] = color
            np.write()


async def clear_neopixel_rgb(data):
    print('Clearing all neopixels!')
    for i in range(config.pixel_count):
        np[i] = (0, 0, 0)
        
    np.write()

def PrintWifiSatus(number):
    #https://mpython.readthedocs.io/en/v2.2.1/library/micropython/network.html
    cases = {
        1000: "Wlan status: No connection, no activities", #STAT_IDLE
        1001: "Wlan status: Connecting",
        202: "Wlan status: Failed due to password error",
        201: "Wlan status: Failed, because there is no access point reply",
        1010: "Wlan status: Connected",
        203: "Wlan status: STAT_ASSOC_FAIL",
        204: "Wlan status: Handshake timeout",
        200: "Wlan status: Timeout"
        # Add more cases as needed
    }
    # Get the message from the dictionary based on the number (status code)
    # If the number is not found, return a default message
    message = cases.get(number, "Wlan status: Unknown Status Code")
    
    # Print the message or perform any other action needed
    print(message)

def main():
    print("""
     ___ ____      _    
    |_ _|  _ \    / \   
     | || |_) |  / _ \  
     | ||  _ <  / ___ \ 
    |___|_| \_\/_/   \_\

    """)
    print('Boot up IRA version: {}'.format(config.device_version), "running on Python version:", sys.version)
    print('Deviceid:', config.device_id)
    print('Device Name:', config.device_name, )
    print('Hardware:', config.device_hardware)
    
    print('Pinout number:', config.pinOutNumber)
    print('Leds count:', config.pixel_count)
    
    
    #ACTIVATE WIFI, CONNECT TO ROUTER
    wlan = network.WLAN(network.STA_IF) #Stands for Station Interface
    
    wlan.active(False)  # important doesn't hurt and will reset the WIFI to a known state.
    #wlan.disconnect()
    
    wlan.active(True) # activate the interface
    
    if wlan.isconnected(): # check if the station is connected to an AP
        print('We are already in connected state with wifi.')
    else:
        print('We are not connected to network...')
        
        #sta_if.config(hidden=True) #@Hackerspace the wifi is hidden.
        print("Connecting to router...")
        wlan.connect(config.wifi_ssid, config.wifi_password)  # connect to an AP
        
        while not wlan.isconnected(): # wait till we are really connected
            s=wlan.status()
            PrintWifiSatus(s)
            time.sleep(2) #  you can also just put pass here        
    
    print("Retrieving Network Configuration from: [", config.wifi_ssid, "].")
    print('Network config:', wlan.ifconfig())
    print('Received signal strength indication:',wlan.status('rssi'), "dBm");
    
    #Send clear event when we do soft reboot, (leds can still be lighting up)
    clear_neopixel_rgb(None)
    # Set all pixels to white
    np.fill((255, 255, 255))
    np.write()  # Don't forget to call write() to actually update the LEDs

    i = Ira(config.device_id, config.device_name, config.device_hardware, config.device_version)
    i.register_handler('set_pixel', set_neopixel_rgb)
    i.register_handler('clear_pixels', clear_neopixel_rgb)

    asyncio.run(i.listen())
    print('Listening to ira messages')

    asyncio.get_event_loop().run_forever()

main()