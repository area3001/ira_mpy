# Managing your devices

## Firmware
### checking the version
```shell
nats req area3001.ira.daan.devices.c82b968b1744.version ''
```

### update firmware
```shell
nats pub area3001.ira.daan.devices.c82b968b1744.update ''
```

## Device Operations
### reboot the device
```shell
nats pub area3001.ira.daan.devices.c82b968b1744.reboot ''
```