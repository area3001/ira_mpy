# IRA Micropython
This repository contains code to incorporate micropython with the IRA setup.

## Getting Started
Before you can do anything useful, you will need to setup your local environment and the ESP32 controller. Detailed 
instructions can be found in the [Getting Started](GETTING_STARTED.md) guide.

But installing things alone is not enough, you will also need to configure your device. This is described in the
[Configuration Guidelines](CONFIGURE.md).

## Design
The design of the system is described in the [Design](DESIGN.md) document.

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