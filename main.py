import time

from ira import config
import asyncio
import network

from ira.device import Device
from ira.link import link
from ira.state import StateMachine
from ira.uplink import Uplink

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
    print('Device Version:', cfg.get_device_version())
    print('Hardware:', cfg.get_device_hardware())
    print('Wifi SSID:', cfg.get_wifi_ssid(), 'Hidden:', cfg.get_wifi_hidden())
    print('NATS Server:', cfg.get_server())

    upl = Uplink(cfg)
    dev = Device(cfg)

    # load the device configuration
    dev.load()

    sm = StateMachine(cfg, upl, dev)
    asyncio.run(sm.run())

    #
    #
    # if not upl.is_connectable():
    #     print('not configured')
    # else:
    #     link(upl, dev)
    #     asyncio.run(upl.connect())
    #     print('listening to ira messages')

    asyncio.get_event_loop().run_forever()

main()