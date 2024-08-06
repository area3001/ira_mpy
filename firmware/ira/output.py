import json


def link_output(upl, dev):
    upl.register_handler('output.rgb', lambda data: set_rgb(upl, dev, data))
    upl.register_handler('output.dmx', lambda data: patch_dmx(upl, dev, data))
    upl.register_handler('output.dmx_raw', lambda data: set_dmx(upl, dev, data))
    upl.register_handler('output.configure', lambda data: configure(upl, dev, data))
    upl.register_handler('output.config', lambda data: config(upl, dev, data))


def config(upl, dev, data):
    """
    Print the configuration of the output channels
    """
    return dev.output_config


def configure(upl, dev, data):
    if not data or len(data) == 0:
        return

    payload = json.loads(data)
    if 'channel' not in payload:
        raise ValueError('channel is required')

    if 'config' not in payload:
        raise ValueError('config is required')

    channel = payload['channel']
    settings = payload['config']

    dev.register_output(channel, settings)

    return {"success": True}


def set_rgb(upl, dev, data):
    affected_channels = set([])

    pairs = data.split(' ')
    for i in range(0, len(pairs)):
        particles = pairs[i].split('#')
        if len(particles) != 3:
            print("invalid particles format")
            return {"error": "invalid particles format"}

        # particle 3 is the color
        color = particles[2]

        color = tuple(int(color[i:i + 2], 16) for i in range(0, len(color), 2))

        channel = particles[0]
        addr = particles[1]
        if channel == '*':
            # -- iterate all channels
            affected_channels = dev.outputs.keys()
            for channel in affected_channels:
                if addr == '*':
                    # set all pixels to the same color
                    for i in range(0, dev.outputs[channel].rgb_length()):
                        dev.outputs[channel].rgb_set(i, color)
                else:
                    a = int(addr)
                    if 0 <= a < dev.outputs[channel].rgb_length():
                        # set a specific pixel to the color
                        dev.outputs[channel].rgb_set(a, color)

        else:

            affected_channels.add(channel)

            if addr == '*':
                # set all pixels
                for i in range(0, dev.outputs[channel].rgb_length()):
                    dev.outputs[channel].rgb_set(i, color)
            else:
                a = int(addr)
                if 0 <= a < dev.outputs[channel].rgb_length():
                    # set a specific pixel to the color
                    dev.outputs[channel].rgb_set(a, color)

    # flush the changes to the output
    for channel in affected_channels:
        dev.outputs[channel].rgb_write()

    return {"success": True}


def set_dmx(upl, dev, data):
    # check if a dmx output is available
    if 'dout' not in dev.outputs:
        raise ValueError('No DMX output available')

    dev.outputs['dout'].set_dmx(data)


def patch_dmx(upl, dev, data):
    # check if a dmx output is available
    if 'dout' not in dev.outputs:
        raise ValueError('No DMX output available')

    dev.outputs['dout'].patch_dmx(data)


class Output:
    def set_rgb(self, data):
        pass

    def rgb_set(self, pixel, color_tuple):
        pass

    def rgb_write(self):
        pass

    def rgb_length(self):
        pass

    def set_dmx(self, data):
        """
        Set the DMX data and send it.

        The provided data needs to be exactly 512 bytes long. If longer, the data will be truncated.
        """
        pass

    def patch_dmx(self, data):
        """
        Path the dmx data and send it.

        The provided data needs to be a dict using the following format:
        `{channel:value}`

        The channel is the DMX channel to be patched and the value is the value to be set.
        """
        pass

    def close(self):
        pass


