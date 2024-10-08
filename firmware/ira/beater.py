import asyncio
import gc
import json
import esp32

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
        if not self._upl.is_connected():
            print("not beating; not connected")
            return

        try:
            await self._upl.c.publish(
                'area3001.ira.{}.devices.{}'.format(self._cfg.get_device_group(), self._cfg.get_device_name()),
                self._heartbeat_msg())
        except Exception as e:
            print('Error sending heartbeat:', e)
            gc.collect()
            return

    def _heartbeat_msg(self):
        return json.dumps({
            'name': self._cfg.get_device_name(),
            'hardware': self._cfg.get_device_hardware(),
            'version': self._cfg.get_device_version(),
            'handlers': [k for k in self._upl.handlers.keys()],
            'mem_free': gc.mem_free(),
            'mem_alloc': gc.mem_alloc(),
            'rssi': self._upl.get_rssi(),
            'temperature': (esp32.raw_temperature() - 32.0) / 1.8
        })
