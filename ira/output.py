import asyncio
import sys

from machine import Pin
from neopixel import NeoPixel


class Output:
    def set_rgb(self, data):
        raise NotImplementedError

    def rgb_set(self, pixel, color_tuple):
        raise NotImplementedError

    def rgb_write(self):
        raise NotImplementedError

    def rgb_length(self):
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
        for i in range(0, len(self.np)):
            self.np[i] = (0, 0, 0)
        self.np.write()

        self._fx = None

    def run_fx(self, data):
        name = data['name']

        if self._fx:
            self._fx.cancel()

        self._fx = asyncio.create_task(self._run_effect(name, data))

    def stop(self):
        if self._fx:
            self._fx.cancel()
            self._fx = None

        for i in range(0, len(self.np)):
            self.np[i] = (0, 0, 0)
        self.np.write()


    async def _run_effect(self, name, data):
        try:
            exec('import fx.' + name, {})
            await sys.modules['fx.' + name].run(self, data)
        except Exception as e:
            print(e)
            sys.print_exception(e)

    def rgb_length(self):
        return len(self.np)

    def rgb_set(self, pixel, color_tuple):
        self.np[pixel] = color_tuple

    def rgb_write(self):
        self.np.write()

    def set_rgb(self, data):
        print("setting neopixel data", data)
        pairs = data.split(' ')
        for i in range(0, len(pairs)):
            addr_color = pairs[i].split('#')
            if len(addr_color) != 2:
                print("invalid color format")
                return {"error": "invalid color format"}

            color = addr_color[1]
            color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

            if addr_color[0] == '*':
                # set all pixels
                for i in range(0, len(self.np)):
                    self.rgb_set(i, color)

            else:
                addr = int(addr_color[0])
                if addr >= len(self.np):
                    # address out of range
                    print("address out of range")
                    return {"error": "address out of range"}

                self.rgb_set(addr, color)

        self.rgb_write()
        return {"success": True}
