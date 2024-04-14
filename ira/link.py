import json


def link(upl, dev):
    upl.register_handler('rgb', lambda channel, data: set_rgb(upl, dev, channel, data))
    upl.register_handler('configure', lambda channel, data: configure(upl, dev, channel, data))
    upl.register_handler('config', lambda channel, data: config(upl, dev, channel))
    upl.register_handler('fx', lambda channel, data: run_fx(upl, dev, channel, data))
    upl.register_handler('stop', lambda channel, data: stop_fx(upl, dev, channel, data))

    upl.register_handler('fx_list', lambda channel, data: list_fx(upl, dev, channel, data))
    upl.register_handler('fx_load', lambda channel, data: load_fx(upl, dev, channel, data))


def config(upl, dev, channel):
    return dev.output_config[str(channel)]


def configure(upl, dev, channel, data):
    dev.register_output(str(channel), data)


def set_rgb(upl, dev, channel, data):
    if str(channel) in dev.outputs:
        return dev.outputs[str(channel)].set_rgb(data)

    return {'error': 'channel not found'}


def list_fx(upl, dev, channel, data):
    return dev.fx.list()


def load_fx(upl, dev, channel, data):
    ffx = json.loads(data)
    dev.fx.load(ffx['name'], ffx['source'])


def run_fx(upl, dev, channel, data):
    if str(channel) in dev.outputs:
        dev.outputs[str(channel)].run_fx(json.loads(data))
    else:
        return {'error': 'channel not found'}


def stop_fx(upl, dev, channel, data):
    if str(channel) in dev.outputs:
        dev.outputs[str(channel)].stop()
    else:
        return {'error': 'channel not found'}
