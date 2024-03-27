

class Protocol:
    def __init__(self, device):
        self.device = device

    async def set_neopixel_rgb(self, data):
        # check for valid data like this ['set_pixel', '0 #00ff00']
        if len(data) != 2:
            return False

        # get the device identifier
        parts = data[1].split(' ')
        if len(parts) != 2:
            return False

        dev_id = int(parts[0])
        if dev_id < 0 or dev_id >= len(self.device.outputs):
            return False
        dev = self.device.outputs[dev_id]

        pairs = data[1].split(',')
        for i in range(1, len(parts)):
            addr_color = pairs[i].split('#')
            if len(addr_color) != 2:
                return False

            addr = int(addr_color[0])
            if addr >= len(dev):
                # address out of range
                return False

            color = addr_color[1]
            color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
            dev[addr] = color

        dev.write()

    async def clear_neopixel_rgb(self, data):
        if len(data) != 2:
            return False

        dev_id = int(data[1])
        if dev_id < 0 or dev_id >= len(self.device.outputs):
            return False

        dev = self.device.outputs[dev_id]

        for i in range(len(dev) - 1):
            dev[i] = (0, 0, 0)

        dev.write()