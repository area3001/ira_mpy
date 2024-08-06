import json
import machine

import uota


def link_system(upl, dev):
    upl.register_handler('version', lambda data: version(upl, dev, data))
    upl.register_handler('reboot', lambda data: reboot(upl, dev, data))
    upl.register_handler('update', lambda data: update(upl, dev, data))


def reboot(upl, dev, data):
    machine.reset()

def version(upl, dev, data):
    return json.dumps({'version': dev.version, 'has_update': uota.check_for_updates()})

def update(upl, dev, data):
    if uota.check_for_updates():
        uota.install_new_firmware()
        machine.reset()