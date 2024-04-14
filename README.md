# IRA Micropython
This repository contains code to incorporate micropython with the IRA setup.

## Getting Started
- [Install micropython on your ESP32 controller](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)
- install Thonny using homebrew `brew install thonny` or from [here](https://github.com/thonny/thonny/releases)
- configure Thonny to connect to your ESP32 device
- make sure the Files view in thonny is visible, you will use it a lot
- Clone this repository to a location of your choosing
- copy all files in the location of your choosing to the ESP32 using Thonny (select files, right-click, Upload to /)

## Configuring Wifi
Make sure you have uploaded the latest version
Connect to the ESP32 and enter the following commands on the REPL
```python
from ira.config import Config
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
nats pub area3001.ira.<your-group>.devices.<your-id>.output.0.configure '{"kind": "neopixel", "pin": 2, "length": 26}'
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

## Operating the outputs
### Setting the color of a neopixel
```commandline
nats req "area3001.ira.daan.devices.240ac4471ed0.output.1.rgb" "0#000033 1#003300 2#330000"
```

In case you want to set all pixels to a color, you can use `*` as the pixel number:
```commandline
nats req "area3001.ira.daan.devices.240ac4471ed0.output.1.rgb" "*#000033"
```

### Clearing the pixels
```commandline
nats req "area3001.ira.daan.devices.240ac4471ed0.output.1.rgb" "*#000000"
```