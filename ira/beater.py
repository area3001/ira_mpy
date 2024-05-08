import asyncio
import gc
import json
import ntptime
import time

class Beater:
    def __init__(self, cfg, upl, dev):
        self._cfg = cfg
        self._upl = upl
        self._dev = dev

    async def run(self):
        while True:
            await self.beat()
            await asyncio.sleep(10)

    async def beat(self):
        await self._upl.c.publish(
            'area3001.ira.{}.devices.{}'.format(self._cfg.get_device_group(), self._cfg.get_device_id()),
            self._heartbeat_msg())

    def _heartbeat_msg(self):
        ntptime.host = 'be.pool.ntp.org'
        ntptime.settime()

        return json.dumps({
            'name': self._cfg.get_device_name(),
            'hardware': self._cfg.get_device_hardware(),
            'version': self._cfg.get_device_version(),
            'handlers': [k for k in self._upl.handlers.keys()],
            'mem_free': gc.mem_free(),
            'mem_alloc': gc.mem_alloc(),
            'time': time.localtime(),
        })
