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
  * FX > DMX out with white (RGBW, RGBW, RGBW, ...), same FX as for LEDtape
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
### NATS Server
Currently during development we connect to `nats://demo.nats.io:4222`. This is a public server and is not meant for 
production use. In the future we will have our own server.

### Individual & Group control
There are 2 ways of controlling a IRA, either directly or by controlling them in group.
An IRA can be part of 1 group at the moment, this could be extended in the future.

#### Addressing a group of devices
All devices in a group can be sent or listened to through they group subject `area3001.ira.__group__.devices.all`. The group is
defined in the configuration of the device.

#### Addressing a single device
A single device can be sent or listened to through the device subject `area3001.ira.__group__.devices.__id__`. The id is
defined in the configuration of the device.

### Device
A device has several endpoints that can be communicated with. These are:
- `output` = this is the output of the device
- `config` = this is the configuration of the device
- `fx` = device-local effects
- `input` = this is the input of the device

Endpoints are added to the device subject as follows:
- `area3001.ira.__group__.devices.all.__endpoint__` for targeting an endpoint for multiple devices
- `area3001.ira.__group__.devices.__id__.__endpoint__` for targeting an endpoint for one device

### The `output` endpoint
The output endpoint is used to control the output of the device. Messages sent to this endpoint are commands to control
what is being outputted. Multiple outputs can be configured on a device, each of a different or the same type.

An output can be addressed by adding its identifier to the subject; `area3001.ira.__group__.devices.__id__.output.__output_id__`.

#### RGB Output
The RGB output is used to control the color of the output. It is particularly useful for controlling LED strips.

##### Setting RGB Output
```commandline
nats req "area3001.ira.daan.devices.240ac4471ed0.output.1.rgb" "0#000033 1#003300 2#330000"
```

In case you want to set all pixels to a color, you can use `*` as the pixel number:
```commandline
nats req "area3001.ira.daan.devices.240ac4471ed0.output.1.rgb" "*#000033"
```

##### Clearing RGB Output
```commandline
nats req "area3001.ira.daan.devices.240ac4471ed0.output.1.rgb" "*#000000"
```


# Outdated

#### Subtopics
For each of the above topics we have the following split, these are processed with a listener wildcard so that we only need listeners subscribed for the topics above:
- <topic>.<1 through 8>.rgb = set raw RGB mode active, disable FX mode and directly control pixels
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
