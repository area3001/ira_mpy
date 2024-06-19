import json

from ira import dmx
from ira.output import Output


class DmxOutput(Output):
    def __init__(self, cfg):
        if 'port' not in cfg:
            raise ValueError("port is required")

        port = int(cfg['port'])

        self.length = int(cfg['length']) if "length" in cfg else 1
        self.bpp = int(cfg['bpp']) if "bpp" in cfg else 4
        self.universe = dmx.Universe(port)
        self.universe.attach()

        self.buffer = {}

    def close(self):
        print("Closing DMX output")
        self.universe.close()

    def set_dmx(self, data):
        pl = json.loads(data)
        self.universe.set_data(pl)
        # self.universe.write()

    def patch_dmx(self, data):
        pl = json.loads(data)
        self.universe.set_channels(pl)

    def rgb_length(self):
        return self.length

    def rgb_set(self, pixel, color_tuple):
        offset = (pixel * self.bpp) + 1

        for i in range(0, len(color_tuple)):
            self.buffer[str(offset + i)] = color_tuple[i]

    def rgb_write(self):
        self.universe.set_channels(self.buffer)
        self.buffer = {}


