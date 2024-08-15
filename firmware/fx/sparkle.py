import asyncio
import random

def fill(string, color):
    for i in range(0, string.rgb_length()):
        string.rgb_set(i, color)

## Simple pixel effect that lights up each pixel in blue
## run with:
## fx.run '{"name": "sparkle", "output": "1"}'
## make sure the output exists and is passed as a string
##
async def run(device, config):
    print("running sparkle fx on", config['output'])
    output = device.outputs[config['output']]
    length = output.rgb_length()
    
    while True:
        fill(output, (0,0,0))
        output.rgb_set(random.randint(0,length-1),(255,255,255))
        output.rgb_write()
        await asyncio.sleep_ms(50)
        
