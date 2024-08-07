# Originally from pyb_dmx from clacktronics (https://github.com/clacktronics/pyb_dmx/)
#
# Needs to be rewritten to asyncio
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
        self.dirty = False

    def close(self):
        self.dmx_uart.deinit()

    def set_data(self, data):
        if len(data) > 512:
            data = data[:512]

        self.dmx_message[1:len(data)] = data
        self.dirty = True

    def set_channels(self, message):
        """
        a dict and writes them to the array
        format {channel:value}
        """
        for ch in message:
            self.dmx_message[int(ch)] = message[ch]

        self.dirty = True

    async def write(self):
        self.dmx_uart.sendbreak()

        while not self.dmx_uart.txdone():
            sleep_us(100)

        self.dmx_uart.write(self.dmx_message)
        self.dirty = False

        # await asyncio.sleep_ms(22)
        await asyncio.sleep_ms(22)

    def attach(self):
        asyncio.create_task(self._loop())

    async def _loop(self):
        while True:
            if self.dmx_uart.txdone():
                await self.write()
            else:
                await asyncio.sleep_ms(1)
