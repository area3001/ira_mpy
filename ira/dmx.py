# Originally from pyb_dmx from clacktronics (https://github.com/clacktronics/pyb_dmx/)
# Rewritten to asyncio
# @TODO: still needs a patch in micropython for a bigger default messsage buffer of at least 513 bytes

import asyncio
from array import array
from time import sleep_us

from machine import UART, Pin

class Universe():
    def __init__(self, port):
        self.dmx_uart = UART(port, rx=23, tx=13, rts=18, cts=19)
        self.dmx_uart.init(250000, bits=8, parity=None, stop=2)

        # First byte is always 0, 512 after that is the 512 channels
        self.dmx_message = array('B', [0] * 513)

    def set_data(self, data):
        if len(data) > 512:
            data = data[:512]

        self.dmx_message[1:len(data)] = data

    def set_channels(self, message):
        """
        a dict and writes them to the array
        format {channel:value}
        """
        for ch in message:
            self.dmx_message[ch] = message[ch]

    def attach(self):
        asyncio.create_task(self._loop())

    async def _loop(self):
        while True:
            if self.dmx_uart.txdone():
                self.dmx_uart.sendbreak()

                while not self.dmx_uart.txdone():
                    sleep_us(100)

                self.dmx_uart.write(self.dmx_message)

                await asyncio.sleep_ms(22)
            else:
                await asyncio.sleep_ms(1)
