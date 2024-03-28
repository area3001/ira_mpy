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
- NATS
- IR (opt)
- OTA (opt)

### Core1
- Ledtape
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
- <topic>.dmx.rgb
- <topic>.dmx.rgbw
- <topic>.dmx.rgbfx
- <topic>.dmx.rgbwfx

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

## Documentation rules
We adopt 2 styles of documentation:
- MARKDOWN: this is used for files like this README
- DOXYGEN: this is used for inline documentation in the code
  
## TODO
- Implement topic structure according to individual outputs
- Implement FX
- Implement DMX
- Implement Dual Core support
- Command white_pixels
- Command config_change
- Command set_pixel : check if pixel ID is not larger then pixel_count
