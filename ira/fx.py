import binascii
import os


class FxEngine:
    def __init__(self, dev):
        self._dev = dev
        self._current = None

    def list(self):
        return [file[:-3] for file in os.listdir('/fx') if file.endswith('.py') and file != '__init__.py']

    def load(self, name, sourcecode):
        with open('/fx/' + name + '.py', 'w') as f:
            f.write(binascii.a2b_base64(sourcecode).decode('utf-8'))
        print('loaded effect', name)
