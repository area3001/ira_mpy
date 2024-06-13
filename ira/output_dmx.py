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

    def set_dmx(self, data):
        pl = json.loads(data)
        self.universe.set_data(pl)
        # self.universe.write()

    def patch_dmx(self, data):
        pl = json.loads(data)
        self.universe.set_channels(pl)

    def close(self):
        self.universe.close()

    def rgb_length(self):
        return self.length

    def rgb_set(self, pixel, color_tuple):
        channels = {}
        for i in range(0, len(color_tuple)):
            channels[str(i * pixel)] = color_tuple[i]

        self.universe.set_channels(channels)

    def rgb_write(self):
        pass


