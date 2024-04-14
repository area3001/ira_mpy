
def link(upl, dev):
    upl.register_handler('rgb', lambda channel, data: set_rgb(upl, dev, channel, data))
    upl.register_handler('configure', lambda channel, data: configure(upl, dev, channel, data))
    upl.register_handler('config', lambda channel, data: config(upl, dev, channel))


def config(upl, dev, channel):
    return dev.output_config[str(channel)]


def configure(upl, dev, channel, data):
    dev.register_output(str(channel), data)


def set_rgb(upl, dev, channel, data):
    if str(channel) in dev.outputs:
        return dev.outputs[str(channel)].set_rgb(data)

    return {'error': 'channel not found'}