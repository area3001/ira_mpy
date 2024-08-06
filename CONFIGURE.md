# Configure Your Device

## Configuring Wifi
Make sure you have uploaded the latest version
Connect to the ESP32 and enter the following commands on the REPL

```python
from firmware.ira import Config
cfg = Config()
cfg.set_device_name("<your-device-name>")
cfg.set_device_group("<your-device-group>")
cfg.set_device_hardware("<the kind of device>")
cfg.set_device_version("<the version of the device hardware>")
cfg.set_wifi_ssid("<your-ssid>")
cfg.set_wifi_password("<your-pwd>")
cfg.persist()
```

Now reboot the ESP32 and it should connect to your wifi network and even to NATS. You can validate this either by 
looking at the serial output, or by consuming the `area3001.ira.>` subject on the NATS server by running the following 
command:

```commandline
nats sub 'area3001.ira.>'
```

## Configure outputs
Before you can do anything useful with the outputs, you need to configure them. You can do this by sending a message to
the device with the configuration. For example, to configure output 0 with a neopixel on pin 2 and a length of 26, you 
can send the following message:
```commandline
nats pub area3001.ira.<your-group>.devices.<your-id>.output.configure '{"channel": "1", "config":{"kind": "neopixel", "pin": 2, "length": 10}}'
```

In theory, this should also allow for all devices in a group to be configured at once by targetting the group instead
of a specific device. YMMV, not tested at the moment.

The following output types are supported:
- neopixel
- dmx (soon to be added)

### Neopixel
Configuring a neopixel output can be done by sending a message like the next one:
```json
{
  "kind": "neopixel",
  "pin": 2,
  "length": 26
}
```
this will configure the output to be a neopixel output on pin 2 with a length of 26 leds.

There are a few extra settings to be provided in case your pixels need it:
```json
{
  "kind": "neopixel",
  "pin": 2,
  "length": 26,
  "bpp": 0.5,
  "timing": 1
}
```
- `bpp` is the number of bits per pixel, this is usually 4 for RGBW leds and 3 for RGB leds with 3 being the default value
- `timing` is the timing to use, this is usually 1 for WS2812 leds and 0 for SK6812 leds with 1 being the default value

### DMX
Configuring a DMX output can be done by sending a message like the next one:

```shell
nats req area3001.ira.default.devices.c82b968b160c.output.configure '{"channel": "dmx", "config": {"kind": "dmx", "port": "1"}}'
```

Sending DMX data:
```shell
nats pub area3001.ira.default.devices.c82b968b160c.output.dmx '{"1": 128, "2": 0, "3": 128, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 255, "10": 0, "11": 255, "12": 255, "13": 255, "14": 0, "15": 0, "16": 0, "17": 0}'
```