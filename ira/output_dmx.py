import json

from ira import dmx
from ira.output import Output


class DmxOutput(Output):
    def __init__(self, cfg):
        if 'port' not in cfg:
            raise ValueError("port is required")

        port = int(cfg['port'])

        self.universe = dmx.Universe(port)
        self.universe.attach()

    def set_dmx(self, data):
        pl = json.loads(data)
        self.universe.set_data(pl)

    def patch_dmx(self, data):
        pl = json.loads(data)
        self.universe.set_channels(pl)

    def close(self):
        self.universe.close()


