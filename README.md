# IRA Micropython
This repository contains code to incorporate micropython with the IRA setup.

## Getting Started
- [Install micropython on your ESP32 controller](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)
- install Thonny using homebrew `brew install thonny` or from [here](https://github.com/thonny/thonny/releases)
- configure Thonny to connect to your ESP32 device
- make sure the Files view in thonny is visible, you will use it a lot
- Clone this repository to a location of your choosing
- copy all files in the location of your choosing to the ESP32 using Thonny (select files, right-click, Upload to /)

More info can be found in InstallStepsKoen.txt

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

## Design decisions
- When no network connection, outputs go to white
- LED Tape has two modes:
  * Raw RGB
  * FX = preprogged internal FX
- DMX has 5 modes:
  * Raw frame (513 bytes) > DMX out
  * Raw RGB > DMX out (RGB, RGB, RGB, ...), max 170 channels
  * Raw RGB > DMX out with White (RGBW, RGBW, RGBW, ...), max 128 channels
  * FX > DMX out (RGB, RGB, RGB, ...), same FX as for LEDtape
  * FX > DMX out with white (RGBW, RGBW, RGBW, ...), ssame FX as for LEDtape
 - OTA is desirable, but currently not a priority
 - IR is desirable, but currently not a priority, this can be for:
  * Configuration of the IRA's
  * Interaction with the blasters, however this needs a functional spec., the protocol spec. can be found here: https://github.com/area3001/Timeblaster/tree/main

## Dual Core
The idea is to divide the processing over the cores

### Core0
- FreeRTOS
- WIFI handlers

### Core1
- Micropython
- NATS
- Ledtape

### TBD
- IR (opt)
- OTA (opt)
- DMX (optionally on helper processor?)

## NATS
### Individual & Group control
There are 2 ways of controlling a IRA, either directly or by controlling them in group.
An IRA can be part of 1 group at the moment, this could be extended in the future.

### NATS Server
Currently during development we connect to 

### Topics
#### area3001.ira.<group>.output
area3001.ira.default.output being the default group for IRA's to be part of

#### area3001.ira.<group>.devices.<id>.output
where <id> is device unique and should be set to a hardware unique ID (MAC or serial)

#### Subtopics
For each of the above topics we have the following split, these are processed with a listener wildcard so that we only need listeners subscribed for the topics above:
- <topic>.<1 through 8>.rgb = set raw RGB mode active, disable FX mode and directly control pixelss
- <topic>.<1 through 8>.fx = set FX mode active, disable rawRGB mode and start FX
- <topic>.dmx.raw
- <topic>.dmx.rgb = set DMX output as pixels as RGB or RGBW value (= config variable)
- <topic>.dmx.fx = set DMX output as FX as RGB or RGBW value (= config variable)

### Messages
Multiple commands are combined on each topic.
The message is in ASCII and is space delimited.
It always starts with a command, that can't contain a space for obvious reasons and is then followed by a sequence of command specific data. The command specific data is comma delimited. Example:
- <command><space><command_specific_data>
- 'set_pixel 1#ff0000,20#00ff00' = this sets pixel 1 to Red and pixel 20 to Green

### Commands
- Command Name = CN
- Command Specific Data = CSD
  
#### set_pixel
This is to identify a pixel and set its RGB value.

- CN: 'set_pixel'
- CSD: '<pixel ID>#<Hex RGB value>' example: 23#0000FF sets pixel 23 to Blue.

#### clear_pixels
This sets all pixels to black.

- CN: 'clear_pixels'
- CSD: None

#### white_pixels (TODO)
This sets all pixels to white. This is implemented for panic mode.

- CN: 'white_pixels'
- CSD: None

#### config_change (TODO)
This identifies a parameter and changes its value.

- CN: 'config_change'
- CSD: <config_variable><comma><variable_value>

For the config variables, see the list below.

## Config variables
- led_count
- dmx_mode = options:
  * RGB
  * RGBW
  
## Documentation rules
We adopt 2 styles of documentation:
- MARKDOWN: this is used for files like this README
- DOXYGEN: this is used for inline documentation in the code

## TODO
- Implement topic structure according to individual outputs
- Implement FX
- Implement DMX
- Implement Dual Core support
- Commands  
  * Command white_pixels
  * Command config_change
  * Command set_pixel: check if pixel ID is not larger then pixel_count
  * Command set_pixel: allow for range support, or implement dedicated command 'set_pixel_range 1-10#ff0000,15-30#00ff00'
- Implement OTA
- Implement IR Config
- Implement IR Blaster reactive behavior   
