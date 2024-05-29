import asyncio
import gc

from ira.beater import Beater
from ira.fx import link_fx
from ira.output import link_output


class State:
    def run(self):
        raise NotImplementedError()


class StateMachine:
    def __init__(self, cfg, upl, dev):
        self._cfg = cfg
        self._upl = upl
        self._dev = dev
        self.states = {
            'unconfigured': UnconfiguredState(self),
            'offline': OfflineState(self),
            'connected': ConnectedState(self)
        }

        self.current_state = None
        #self.set_state('unconfigured')

    @property
    def config(self):
        return self._cfg

    @property
    def uplink(self):
        return self._upl

    @property
    def device(self):
        return self._dev

    async def set_state(self, state):
        print('transitioning to:', state)
        asyncio.get_event_loop().stop()
        asyncio.new_event_loop()

        self.current_state = self.states[state]
        asyncio.run(self.current_state)

    async def run(self):
        while True:
            await self.current_state.run(self)


class UnconfiguredState(State):
    def __init__(self, sm):
        self.sm = sm

    async def run(self):
        print("waiting to be configured", end="")
        while True:
            if self.sm.uplink.is_connectable():
                break

            await asyncio.sleep(1)

        self.sm.set_state('offline')


class OfflineState(State):
    def __init__(self, sm):
        self.sm = sm

    async def run(self):
        print("connecting to the network and to nats", end="")
        try:
            while True:
                await self.sm.uplink.connect()
                self.sm.set_state('connected')

        except Exception as e:
            print('Error connecting:', e)
            self.sm.set_state('offline')


class ConnectedState(State):
    def __init__(self, sm):
        self.sm = sm

    async def run(self):
        link_output(self.sm.uplink, self.sm.device)
        link_fx(self.sm.uplink, self.sm.device)

        #beater = Beater(self.sm.config, self.sm.uplink, self.sm.device)
        #asyncio.create_task(beater.run())

        try:
            while True:
                if not self.sm.uplink.is_connected():
                    break

                await asyncio.sleep(5)
                gc.collect()
        finally:
            self.sm.set_state('offline')
