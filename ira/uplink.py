import asyncio
import json
import time

import network
from ira import nats


class Uplink:
    def __init__(self, cfg):
        self.cfg = cfg
        self.wlan = None
        self.c = nats.Connection(cfg.get_server(), debug=True)

        self.handlers = {}

    def is_connectable(self):
        return self.cfg.get_wifi_ssid() is not None

    def is_connected(self):
        return self.wlan is not None and self.wlan.isconnected()

    async def connect(self):
        if self.is_connected():
            print('already connected')
            return

        self.wlan = network.WLAN(network.STA_IF)

        print('ready to connect')
        self.wlan.active(False)
        self.wlan.active(True)

        if self.cfg.get_wifi_hidden() == 1:
            self.wlan.config(ssid=self.cfg.get_wifi_ssid(), hidden=True)

        print("Connecting to router...")
        self.wlan.connect(self.cfg.get_wifi_ssid(), self.cfg.get_wifi_password())

        # CHECK IF CONNECTED TO WLAN
        while not self.wlan.isconnected():
            s = self.wlan.status()
            print_wifi_status(s)
            time.sleep(2)

        print('Network config:', self.wlan.ifconfig())
        await self.c.connect()
        await self.c.subscribe(
            'area3001.ira.{}.devices.{}.output.>'.format(self.cfg.get_device_group(), self.cfg.get_device_id()),
            self._parse_message)
        await self.c.subscribe('area3001.ira.{}.output.>'.format(self.cfg.get_device_group()), self._parse_message)

        asyncio.create_task(self._heartbeat_loop())
        asyncio.create_task(self.c.wait())

    async def close(self):
        await self.c.close()

    def register_handler(self, command, cb):
        self.handlers[command] = cb

    async def _parse_message(self, msg):
        try:
            out_cmd = msg.subject.split('.')[-2:]

            if out_cmd[1] in self.handlers:
                res = await self.handlers[out_cmd[1]](out_cmd[0], msg.data)
                if msg.reply is not None and res is not None:
                    await self.c.publish(msg.reply, res)
            else:
                raise ValueError('Unknown command %s' % out_cmd[1])

        except Exception as t:
            print('Failed to process message \"%s\": %s' % (msg.data, t))

    async def _heartbeat_loop(self):
        while True:
            await self.c.publish('area3001.ira.{}.devices.{}'.format(self.cfg.get_device_group(), self.cfg.get_device_id()), self._heartbeat_msg())
            await asyncio.sleep(10)

    def _heartbeat_msg(self):
        return json.dumps({
            'id': self.cfg.get_device_id(),
        })


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