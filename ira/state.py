import asyncio

import gc

from ira.beater import Beater
from ira.link import link

class State:
    def run(self, cfg, upl, dev):
        raise NotImplementedError()

class StateMachine:
    def __init__(self, cfg, upl, dev):
        self._cfg = cfg
        self._upl = upl
        self._dev = dev
        self.states = {
            'unconfigured': UnconfiguredState(),
            'offline': OfflineState(),
            'connected': ConnectedState()
        }
        self.current_state = None

        self.set_state('unconfigured')

    def set_state(self, state):
        print('transitioning to:', state)
        self.current_state = self.states[state]

    async def run(self):
        while True:
            gc.collect()
            nxt = await self.current_state.run(self._cfg, self._upl, self._dev)
            self.set_state(nxt)


class UnconfiguredState(State):
    def __init__(self):
        pass

    async def run(self, cfg, upl, dev):
        print("waiting to be configured", end="")

        while True:
            print(". ", end="")
            if upl.is_connectable():
                print("") # make sure the newline is printed for further output to work
                return 'offline'
            await asyncio.sleep(5)
            gc.collect()


class OfflineState(State):
    def __init__(self):
        pass

    async def run(self, cfg, upl, dev):
        # -- check if the device is connectable
        if not upl.is_connectable():
            # -- set the state to offline
            return 'unconfigured'

        # -- connect the device
        try:
            await upl.connect()
            return 'connected'
        except Exception as e:
            print('Error connecting:', e)
            return 'offline'


class ConnectedState(State):
    def __init__(self):
        pass

    async def run(self, cfg, upl, dev):
        link(upl, dev)

        beater = Beater(cfg, upl, dev)
        bh = asyncio.create_task(beater.run())

        try:
            while True:
                if not upl.is_connected():
                    break

                await asyncio.sleep(5)
                gc.collect()
        finally:
            bh.cancel()
            return "offline"
