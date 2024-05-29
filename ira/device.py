import json

from machine import Pin
from neopixel import NeoPixel

from ira import output_dmx
from ira import output_neopixel
from ira.fx import FxEngine


class Device:
    def __init__(self, cfg):
        self._cfg = cfg
        self.outputs = {}
        self.output_config = {}

        self.fx = FxEngine(self)

    def load(self):
        self.output_config = self._cfg.get_json('outputs') or {}

        for channel in self.output_config:
            self.load_output(channel, self.output_config[channel])

    def save(self):
        self._cfg.set_json('outputs', self.output_config)
        self._cfg.persist()

    def register_output(self, channel, config):
        # store the configuration
        self.output_config[channel] = config
        self.save()

        # load the output
        self.load_output(channel, self.output_config[channel])

    def load_output(self, channel, cfg):
        if channel in self.outputs:
            self.outputs[channel].close()
            self.outputs[channel] = None

        if 'kind' not in cfg:
            raise ValueError('kind is required')

        if cfg['kind'] == 'neopixel':
            print(f'loading neopixel channel {channel}', cfg)
            self.outputs[channel] = output_neopixel.NeopixelOutput(cfg)
        elif cfg['kind'] == 'dmx':
            self.outputs[channel] = output_dmx.DmxOutput(cfg)
        else:
            raise ValueError('Unknown output kind: {}'.format(cfg['kind']))

    async def set_rgb(self, output, data):
        if output < 0 or output >= len(self.outputs):
            return False

        await self.outputs[output].set_rgb(data)
        return True

    def set_all_rgb(self, data):
        for output in self.outputs:
            self.outputs[output].set_rgb(data)

        return True

