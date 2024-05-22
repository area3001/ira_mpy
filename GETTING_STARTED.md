# Getting Started

## Prerequisites
You will be needing a set of tools in order to develop for the ESP32.
#### Windows
We rely on Winget to make our life a bit easier. Therefor our first step on windows would be to 
[Install](https://learn.microsoft.com/en-us/windows/package-manager/winget/#install-winget) Winget.

Once that's done, we can install the tools we need:
```commandline
winget install --id Git.Git -e --source winget
winget install -e --id Python.Python.3.10
winget install -e --id AivarAnnamaa.Thonny
winget install -e --id GoLang.Go

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install esptool

go install github.com/nats-io/natscli/nats@latest
```

## Clone the repository
```commandline
git clone git@github.com:area3001/ira_mpy.git
```

## Prepare your ESP32
### Download the Micropython firmware
Download the latest [Micropython firmware](https://micropython.org/download/esp32/) for your controller. For the IRA,
we use the [ESP32_GENERIC-SPIRAM firmware](https://micropython.org/resources/firmware/ESP32_GENERIC-SPIRAM-20240222-v1.22.2.bin)

### Determine the port your controller is connected to
#### Windows
Under Windows, this is called a COM port. You can find this in the device manager under Ports (COM & LPT).
To make things easier, we will export this to an environment variable:
```commandline
set COM_PORT=COM4
```
#### Mac & Linux
Under Mac & Linux, this is called a tty port. You can find this by running the following command:
```commandline
ls /dev/tty*
```
You should be looking for something like `/dev/ttyUSB0` or `/dev/ttyS0`. We will export this to an environment variable:
```commandline
export COM_PORT=/dev/ttyUSB0
```

### Erase the flash and flash micropython
#### Windows
```commandline
esptool.exe --chip esp32 --port %COM_PORT% erase_flash
esptool.exe --chip esp32 --port %COM_PORT% --baud 460800 write_flash -z 0x1000 "file_location\___.bin"
```

#### Mac & Linux
```commandline
esptool.py --chip esp32 --port $COM_PORT erase_flash
esptool.py --chip esp32 --port $COM_PORT --baud 460800 write_flash -z 0x1000 "file_location\___.bin"
```

## Copy the files to the ESP32
Use Thonny or Pycharm to copy the following files to the ESP32:
- main.py
- fx
- ira

## Configure your device
In order to use your device, you will have to configure it first. This means configuring the wifi and the outputs.
Take a look at the [Configuration Guidelines](CONFIGURE.md) for more information.

## IDE support
### Thonny
#### Windows
```commandline
winget install -e --id AivarAnnamaa.Thonny
```

### Pycharm
- Download PyCharm from https://www.jetbrains.com/pycharm/
- Install the Micropython plugin in PyCharm

This was based on https://mischianti.org/micropython-with-esp8266-and-esp32-flashing-firmware-and-using-pycharm-ide-3/
