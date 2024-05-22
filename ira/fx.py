import asyncio
import binascii
import json
import os
import sys

_fx = None

def link_fx(upl, dev):
    upl.register_handler('fx.run', lambda data: run_fx(upl, dev, data))
    upl.register_handler('fx.list', lambda data: list_fx(upl, dev, data))
    upl.register_handler('fx.load', lambda data: load_fx(upl, dev, data))
    upl.register_handler('fx.stop', lambda data: stop_fx(upl, dev, data))


def list_fx(upl, dev, data):
    return dev.fx.list()


def load_fx(upl, dev, data):
    ffx = json.loads(data)
    dev.fx.load(ffx['name'], ffx['source'])


def run_fx(upl, dev, data):
    global _fx

    pl = json.loads(data)
    name = pl['name']

    if _fx:
        _fx.cancel()

    _fx = asyncio.create_task(_run_effect(name, data))


def stop_fx(upl, dev, data):
    global _fx

    if _fx:
        _fx.cancel()
        _fx = None


async def _run_effect(name, data):
    try:
        exec('import fx.' + name, {})
        await sys.modules['fx.' + name].run(self, data)
    except Exception as e:
        print(e)
        sys.print_exception(e)


class FxEngine:
    def __init__(self, dev):
        self._dev = dev
        self._current = None

    def list(self):
        return [file[:-3] for file in os.listdir('/fx') if file.endswith('.py') and file != '__init__.py']

    def load(self, name, sourcecode):
        with open('/fx/' + name + '.py', 'w') as f:
            f.write(binascii.a2b_base64(sourcecode).decode('utf-8'))
        print('loaded effect', name)
