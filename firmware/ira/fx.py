import asyncio
import binascii
import json
import os
import sys


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
    return {"success": True, "msg": "effect loaded"}


def run_fx(upl, dev, data):
    pl = json.loads(data)
    dev.fx.run(pl['name'], pl, upl.logger)
    return {"success": True, "msg": "effect start requested"}


def stop_fx(upl, dev, data):
    dev.fx.stop()
    return {"success": True, "msg": "effect stopped"}


async def _run_effect(dev, name, data, logger):
    try:
        exec('import fx.' + name, {})

        await logger.log("info", "effect {} imported".format(name))

        await sys.modules['fx.' + name].run(dev, data)
    except Exception as e:
        await logger.log("error", "failed to run effect: {}".format(e))
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

    def run(self, name, args, logger):
        # stop the current fx
        self.stop()

        # start the new fx
        self._current = asyncio.create_task(_run_effect(self._dev, name, args, logger))

    def stop(self):
        if self._current:
            self._current.cancel()
            self._current = None
