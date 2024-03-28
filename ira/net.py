

class Protocol:
    def __init__(self, device):
        self.device = device

    async def set_rgb(self, output, data):
        if output < 0 or output >= len(self.device.outputs):
            return False
        dev = self.device.outputs[output]

        pairs = data.split(' ')
        if output == 'dmx':
            return await self._set_rgb_dmx(output, pairs)
        else:
            return await self._set_rgb_neopixel(output, pairs)

    async def _set_rgb_neopixel(self, dev, pairs):
        for i in range(1, len(pairs)):
            addr_color = pairs[i].split('#')
            if len(addr_color) != 2:
                return False

            addr = int(addr_color[0])
            if addr >= len(dev):
                # address out of range
                return False

            color = addr_color[1]
            color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
            dev[addr] = color

        dev.write()

    async def _set_rgb_dmx(self, dev, pairs):
        pass

