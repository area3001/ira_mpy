from machine import Pin
from neopixel import NeoPixel


class Output:
    def set_rgb(self, data):
        raise NotImplementedError

    def close(self):
        pass


class NeopixelOutput(Output):
    def __init__(self, cfg):
        if 'pin' not in cfg:
            raise ValueError('pin is required')
        if 'length' not in cfg:
            raise ValueError('length is required')

        pin = cfg['pin']
        length = cfg['length']
        bpp = cfg.get('bpp', 3)
        timing = cfg.get('timing', 1)

        self.np = NeoPixel(Pin(pin), length, bpp=bpp, timing=timing)

    def set_rgb(self, data):
        pairs = data.split(' ')
        for i in range(1, len(pairs)):
            addr_color = pairs[i].split('#')
            if len(addr_color) != 2:
                return False

            addr = int(addr_color[0])
            if addr >= len(self.np):
                # address out of range
                return False

            color = addr_color[1]
            color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
            self.np[addr] = color

        self.np.write()
