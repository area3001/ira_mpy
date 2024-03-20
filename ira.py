import asyncio
import network
import json
import ubinascii

import nats
import config

class Ira:
    def __init__(self, id, name, hw_type, hw_version, group="default", url=config.natsServer):
        self.id = id
        self.name = name
        self.group = group
        self.wlan = network.WLAN(network.STA_IF)
        self.hw_type = hw_type
        self.hw_version = hw_version
        self.mode = 0
        
        self.c = nats.Connection(config.natsServer, debug=True)
        self.ht = None
        self.handlers = {}
        
    async def close(self):
        await self.c.close()
        
    def register_handler(self, command, cb):
        self.handlers[command] = cb
        
    async def listen(self):
        await self.c.connect()

        asyncio.create_task(self._heartbeat_loop())
        print('Connected to NATS server:', config.natsServer)

        await self.c.subscribe('area3001.ira.{}.devices.{}.output'.format(self.group, self.id), self._parse_message)
        await self.c.subscribe('area3001.ira.{}.output'.format(self.group), self._parse_message)

        asyncio.create_task(self.c.wait())

    async def _heartbeat_loop(self):
        print('Heartbeat')
        while True:
            await self.c.publish('area3001.ira.{}.devices.{}'.format(self.group, self.id), self._heartbeat_msg())
            print('Sent heartbeat')
            await asyncio.sleep(10)
            
    def _heartbeat_msg(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'group': self.group,
            'hardware': {
                'kind': self.hw_type,
                'version': self.hw_version,
            },
            'network': {
                'mac': ubinascii.hexlify(self.wlan.config('mac')).decode().upper(),
                'ip': self.wlan.ifconfig()[0]
            }
        })
    
    async def _parse_message(self, msg):
        try:
            data = msg.data.split(' ', 1)
            if len(data) == 0:
                return
            
            if data[0] in self.handlers:
                res = await self.handlers[data[0]](data)
                if msg.reply is not None and res is not None:
                    await self.c.publish(msg.reply, res)
            else:
                raise ValueError('Unknown command %s' % data[0])
            
        except Exception as t:
            print('Failed to process message \"%s\": %s' % (msg.data, t))