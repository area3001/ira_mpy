from ira import config
import asyncio
import network

from ira.device import Device

cfg = config.Config()

# nats publish -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'

    

def main():
    print("""
     ___ ____      _    
    |_ _|  _ \    / \   
     | || |_) |  / _ \  
     | ||  _ <  / ___ \ 
    |___|_| \_\/_/   \_\

    """)
    print('Boot up IRA version: {}'.format(cfg.get_device_version()))
    print('Deviceid:', cfg.get_device_id())
    print('Device Name:', cfg.get_device_name())
    print('Hardware:', cfg.get_device_hardware())

    ssid = cfg.get_wifi_ssid()
    if ssid is None:
        print('not configured')

        asyncio.get_event_loop().run_forever()
    else:
        # ACTIVATE WIFI, CONNECT TO ROUTER
        wlan = network.WLAN(network.STA_IF)  # Stands for Station Interface

        if wlan.isconnected():
            print('We are already in connected state with wifi.')
        else:
            print('We are not connected to network...')
            wlan.active(False)
            wlan.active(True)
            #sta_if.config(hidden=True) #@Hackerspace the wifi is hidden.
            print("Connecting to router...")
            wlan.connect(ssid, cfg.get_wifi_password())

            #CHECK IF CONNECTED TO WLAN
            while not wlan.isconnected():
                pass# LOOP UNTIL CONNECTED

        print("Retrieving Network Configuration from: [", ssid, "].")
        print('Network config:', wlan.ifconfig())

        d = Device(cfg.get_device_id(), cfg.get_device_name(), cfg.get_device_hardware(), cfg.get_device_version())
        d.enable_neopixel_support()

        asyncio.run(d.listen())
        print('listening to ira messages')

        asyncio.get_event_loop().run_forever()

main()