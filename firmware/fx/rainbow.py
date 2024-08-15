import asyncio
import random

def wheel(index:int, brightness:int=255) -> tuple(int,int,int):
    # return to start of wheel when getting angles > 360
    index = index % 360
    # make sure brightness is acceptable 
    brightness = max(brightness,1)
    brightness = min(brightness,255)
    if index < 60:
        return (brightness,index*brightness//60,0)
    if index < 120:
        return((120-index)*brightness//60,brightness,0)
    if index < 180:
        return (0,brightness,(index-120)*brightness//60)
    if index < 240:
        return (0,(240-index)*brightness//60,brightness)
    if index < 300:
        return ((index-240)*brightness//60,0,brightness)
    return (brightness,0,(360-index)*brightness//60)


## Simple pixel effect that lights up each pixel in blue
## run with:
## fx.run '{"name": "rainbow", "output": "1"}'
## optional parameters:  "brightness":1-255, "nosparkle":1
## make sure the output exists and is passed as a string
##
async def run(device, config):
    print(config)
    print("running rainbow fx on", config)

    max_length = 0    
    devices = []
    for out_id in device.outputs:
        devices.append((device.outputs[out_id],device.outputs[out_id].rgb_length(),360/device.outputs[out_id].rgb_length()))
        max_length = max(max_length,device.outputs[out_id].rgb_length())

    brightness = 128
    gap=3
    if "brightness" in config and type(config["brightness"]) == int:
        brightness = config["brightness"]

    do_sparkle = True
    if "nosparkle" in config and config["nosparkle"] == 1:
        do_sparkle = False
    
    while True:
        for j in range(max_length):
            for device in devices:
                for i in range(device[1]):
                    device[0].rgb_set(i, wheel(int((i+j)*gap), brightness))
                if do_sparkle and j % 5 == 0:
                    device[0].rgb_set(random.randint(0,device[1]-1),(255,255,255))
                    device[0].rgb_write()
            await asyncio.sleep_ms(33)
        