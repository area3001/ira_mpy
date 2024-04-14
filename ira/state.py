import asyncio


class State:
    def run(self, upl, dev):
        raise NotImplementedError()


class StateMachine:
    def __init__(self, upl, dev):
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
            nxt = await self.current_state.run(self._upl, self._dev)
            self.set_state(nxt)
            await asyncio.sleep(5)


class UnconfiguredState(State):
    def __init__(self):
        pass

    async def run(self, upl, dev):
        print("waiting to be configured", end="")

        while True:
            print(". ", end="")
            if upl.is_connectable():
                print("") # make sure the newline is printed for further output to work
                return 'offline'
            await asyncio.sleep(5)


class OfflineState(State):
    def __init__(self):
        pass

    async def run(self, upl, dev):
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

    async def run(self, upl, dev):
        while True:
            if not upl.is_connected():
                return 'offline'

            await asyncio.sleep(5)