import asyncio
import sys

import machine

from ira import config, system
from ira.beater import Beater
from ira.device import Device
from ira.logger import Logger
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
    version = open('version', 'r').read().strip()

    print('    IRA version {}'.format(version))
    print('Subject: area3001.ira.{}.devices.{}'.format(cfg.get_device_group(), cfg.get_device_name()))
    print('Device ID:', cfg.get_device_id())
    print('Hardware:', cfg.get_device_hardware())
    print('Wifi SSID:', cfg.get_wifi_ssid(), 'Hidden:', cfg.get_wifi_hidden())

    upl = Uplink(cfg)
    dev = Device(cfg, version)

    # load the device configuration
    dev.load()

    # check if the device is connectable
    print("waiting to be configured", end="")
    while not upl.is_connectable():
        print(".", end="")
        await asyncio.sleep(1)

    print("")

    # when it is connectable, connect to the network
    print("connecting to the network and to nats")
    while not upl.is_connected():
        try:
            await upl.connect()
        except Exception as e:
            print('Error connecting:', e)
            sys.print_exception(e)

    output.link_output(upl, dev)
    fx.link_fx(upl, dev)
    system.link_system(upl, dev)

    beater = Beater(cfg, upl, dev)
    asyncio.create_task(beater.run())

    while upl.is_connected():
        await asyncio.sleep(5)

    print('disconnected, restarting')
    machine.reset()

main()
