from machine import Pin
from neopixel import NeoPixel

from ira.output import NeopixelOutput


class Device:
    def __init__(self, cfg):
        self._cfg = cfg
        self.outputs = {}
        self.output_config = {}

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
        if cfg.kind == 'neopixel':
            self.outputs[channel] = NeopixelOutput(cfg)
        else:
            raise ValueError('Unknown output kind: {}'.format(cfg.kind))
