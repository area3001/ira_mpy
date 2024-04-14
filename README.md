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
cfg.set_wifi_ssid('your_ssid')
cfg.set_wifi_password('your_password')
cfg.persist()
```