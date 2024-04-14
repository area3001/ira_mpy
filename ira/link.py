
def link(upl, dev):
    upl.register_handler('rgb', lambda channel, data: set_rgb(upl, dev, channel, data))
    upl.register_handler('configure', lambda channel, data: configure(upl, dev, channel, data))


def configure(upl, dev, channel, data):
    dev.register_output(channel, data)


def set_rgb(upl, dev, channel, data):
    if str(channel) in dev.outputs:
        dev.outputs[channel].set_rgb(data)