import asyncio
import network
import json
import ubinascii

import mpynats as nats

class Ira:
    def __init__(self, id, name, hw_type, hw_version, url='nats://demo.nats.io:4222'):
        self.id = id
        self.name = name
        self.wlan = network.WLAN(network.STA_IF)
        self.hw_type = hw_type
        self.hw_version = hw_version
        
        self.c = nats.Connection('nats://demo.nats.io:4222')
        
    async def listen(self):
        self.c.connect()
        asyncio.run(self._heartbeat_loop())
        print('nats server connected')
    
    async def _heartbeat_loop(self):
        print('heartbeat')
        while True:
            self.c.publish('area3001.ira.{}'.format(self.id), self._heartbeat_msg())
            print('sent heartbeat')
            await asyncio.sleep_ms(30_000)
            
    def _heartbeat_msg(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'hardware': {
                'kind': self.hw_type,
                'version': self.hw_version,
            },
            'network': {
                'mac': ubinascii.hexlify(self.wlan.config('mac')).decode().upper(),
                'ip': self.wlan.ifconfig()[0]
            }
        })
