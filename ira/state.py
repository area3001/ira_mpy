
class State:
    def run(self):
        raise NotImplementedError()


class DisconnectedState(State):
    def __init__(self):
        pass

    async def run(self):
        pass

