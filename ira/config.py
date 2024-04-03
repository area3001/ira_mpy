#  ___ ____      _
# |_ _|  _ \    / \
#  | || |_) |  / _ \
#  | ||  _ <  / ___ \
# |___|_| \_\/_/   \_\
import machine
from esp32 import NVS
import ubinascii


class Config:
    def __init__(self):
        self._nvs = NVS('config')

    def get_device_id(self):
        return ubinascii.hexlify(machine.unique_id()).decode('utf-8')

    def set_device_name(self, value):
        self._nvs.set_blob('device_name', value)

    def get_device_name(self):
        return self.get_string_property('device_name', 32, self.get_device_id())

    def set_device_hardware(self, value):
        self._nvs.get_blob('device_hardware', value)

    def get_device_hardware(self):
        return self.get_string_property('device_hardware', 32, 'UNKNOWN')

    def set_device_version(self, value):
        self._nvs.set_blob('device_version', value)

    def get_device_version(self):
        return self.get_string_property('device_version', 32, '0.0.0')

    def set_wifi_ssid(self, value):
        self._nvs.set_blob('wifi_ssid', value)

    def get_wifi_ssid(self):
        return self.get_string_property('wifi_ssid', 32)

    def set_wifi_password(self, value):
        self._nvs.set_blob('wifi_password', value)

    def get_wifi_password(self):
        return self.get_string_property('wifi_password', 64)

    def set_wifi_hidden(self, value):
        self.set_int_property('wifi_hidden', value)

    def get_wifi_hidden(self):
        return self.get_int_property('wifi_hidden', 0)

    def set_server(self, value):
        self._nvs.set_blob('server', value)

    def get_server(self):
        return self.get_string_property('server', 256, 'nats://demo.nats.io:4222')

    def get_facets(self):
        return self.get_string_property('facets', 256, '')

    def set_facets(self, value):
        self._nvs.set_blob('facets', value)

    def set_int_property(self, key, value):
        self._nvs.set_i32(key, value)

    def get_int_property(self, key, default=None):
        try:
            return self._nvs.get_i32(key)
        except:
            return default

    def set_string_property(self, key, value):
        self._nvs.set_blob(key, value)

    def get_string_property(self, key, max_length=64, default=None):
        try:
            result = bytearray(max_length)
            self._nvs.get_blob(key, result)
            return result.decode('utf-8').trim()
        except:
            return default

    def persist(self):
        self._nvs.commit()


# For MAC
# nats publish -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'

# For Windows (Go) command
# nats-pub -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'
# nats-pub -s nats://demo.nats.io:4222 area3001.ira.default.output 'clear_pixels'