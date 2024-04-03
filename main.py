import time

from ira import config
import asyncio
import network

from ira.device import Device

cfg = config.Config()

# nats publish -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'


def PrintWifiSatus(number):
    # https://mpython.readthedocs.io/en/v2.2.1/library/micropython/network.html
    cases = {
        1000: "Wlan status: No connection, no activities",  # STAT_IDLE
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
    print('Boot up IRA version: {}'.format(cfg.get_device_version()))
    print('Deviceid:', cfg.get_device_id())
    print('Device Name:', cfg.get_device_name())
    print('Hardware:', cfg.get_device_hardware())
    print('Wifi SSID:', cfg.get_wifi_ssid(), 'Hidden:', cfg.get_wifi_hidden())

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

            if cfg.get_wifi_hidden() == 1:
                wlan.config(ssid=ssid, hidden=True)

            print("Connecting to router...")
            wlan.connect(ssid, cfg.get_wifi_password())

            #CHECK IF CONNECTED TO WLAN
            while not wlan.isconnected():
                s = wlan.status()
                PrintWifiSatus(s)
                time.sleep(2)

        print("Retrieving Network Configuration from: [", ssid, "].")
        print('Network config:', wlan.ifconfig())

        d = Device(cfg.get_device_id(), cfg.get_device_name(), cfg.get_device_hardware(), cfg.get_device_version())
        d.enable_neopixel_support()

        asyncio.run(d.listen())
        print('listening to ira messages')

        asyncio.get_event_loop().run_forever()

main()