import asyncio
import json

import network
import machine
import sys

from ira import nats
import uota
from ira.logger import Logger


class Uplink:
    def __init__(self, cfg):
        self.cfg = cfg
        self.wlan = None
        self.c = nats.Connection(cfg.get_server(), debug=False)

        self.endpoints = {}
        self.handlers = {}
        self.logger = Logger(cfg, self)

    def is_connectable(self):
        return self.cfg.get_wifi_ssid() is not None

    def is_connected(self):
        return self.wlan is not None and self.wlan.isconnected()

    def get_rssi(self):
        return self.wlan.status('rssi')

    async def connect(self):
        if self.is_connected():
            print('already connected')
            return

        self.wlan = network.WLAN(network.STA_IF)

        print('ready to connect')
        self.wlan.active(False)
        self.wlan.active(True)

        # if self.cfg.get_wifi_hidden() == 1:
        #     self.wlan.config(ssid=self.cfg.get_wifi_ssid(), hidden=True)

        print("Connecting to router...")
        self.wlan.connect(self.cfg.get_wifi_ssid(), self.cfg.get_wifi_password())

        # CHECK IF CONNECTED TO WLAN
        while not self.wlan.isconnected():
            s = self.wlan.status()
            print_wifi_status(s)
            await asyncio.sleep(1)

        print('Network config:', self.wlan.ifconfig())
        await asyncio.sleep_ms(500)

        if uota.check_for_updates():
            uota.install_new_firmware()
            machine.reset()
        else:
            print("No updates available")

        await self.c.connect()
        await self.c.subscribe(
            'area3001.ira.{}.devices.{}.>'.format(self.cfg.get_device_group(), self.cfg.get_device_name()),
            self._parse_message)
        await self.logger.log('info', 'Listening for incoming messages on area3001.ira.{}.devices.{}.>'.format(
            self.cfg.get_device_group(), self.cfg.get_device_name()))

        await self.c.subscribe(
            'area3001.ira.{}.devices.all.>'.format(self.cfg.get_device_group()),
            self._parse_message)
        await self.logger.log('info', 'Listening for incoming messages on area3001.ira.{}.devices.all.>'.format(
            self.cfg.get_device_group()))

        asyncio.create_task(self.c.wait())



    async def close(self):
        await self.c.close()

    def register_handler(self, subject, cb):
        self.handlers[subject] = cb
        print('registered handler for', subject)

    async def _parse_message(self, msg):
        """
        Parse message from group subject and call the appropriate handler.
        area3001.ira.{}.devices.all.>
        """
        try:
            sub = msg.subject.decode("utf-8").split('.')

            # Get the last parts of the subject, which will denote the actual operation we want to perform
            handler_id = ".".join(sub[5:])

            if handler_id in self.handlers:
                res = self.handlers[handler_id](msg.data)
                if msg.reply is not None and res is not None:
                    await self.c.publish(msg.reply.decode('utf-8'), json.dumps(res))
            else:
                raise ValueError('Unknown command %s' % handler_id)

        except Exception as t:
            await self.logger.log('error', 'Failed to process message "%s": %s' % (msg.data, t))
            sys.print_exception(t)


def print_wifi_status(number):
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