# IRA Micropython
This repository contains code to incorporate micropython with the IRA setup.

## Getting Started
- [Install micropython on your ESP32 controller](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)
- install Thonny using homebrew `brew install thonny` or from [here](https://github.com/thonny/thonny/releases)
- configure Thonny to connect to your ESP32 device
- make sure the Files view in thonny is visible, you will use it a lot
- Clone this repository to a location of your choosing
- copy all files in the location of your choosing to the ESP32 using Thonny (select files, right-click, Upload to /)

Hit CTRL+D to restart device by command inside Thonny

## Things 2 talk about
- Heartbeat -> differnent channel
- Heartbeat -> show version number
- Show message is your device is booted up (or restart is done)
- Device needs to respond if we ask who is out there. Devicename + version number.
- Heartbeat -> timestamp toevoegen -> heartbeat is deel van info