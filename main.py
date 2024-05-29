import asyncio

import ira
from ira import config
from ira.beater import Beater
from ira.device import Device
from ira.state import StateMachine
from ira.uplink import Uplink
from ira import output, fx

cfg = config.Config()

# nats publish -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'


def main():
    asyncio.run(run())
    # pass
    #run()

    #
    #
    # if not upl.is_connectable():
    #     print('not configured')
    # else:
    #     link(upl, dev)
    #     asyncio.run(upl.connect())
    #     print('listening to ira messages')

    #asyncio.get_event_loop().run_forever()

async def run():
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

    upl = Uplink(cfg)
    dev = Device(cfg)

    # load the device configuration
    dev.load()

    # check if the device is connectable
    print("waiting to be configured", end="")
    while not upl.is_connectable():
        print(".", end="")
        await asyncio.sleep(1)

    # when it is connectable, connect to the network
    print("connecting to the network and to nats", end="")
    while not upl.is_connected():
        try:
            await upl.connect()
        except Exception as e:
            print('Error connecting:', e)

    output.link_output(upl, dev)
    fx.link_fx(upl, dev)

    beater = Beater(cfg, upl, dev)
    asyncio.create_task(beater.run())

    while upl.is_connected():
        await asyncio.sleep(5)

    print('disconnected, restarting')

main()
