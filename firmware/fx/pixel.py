import asyncio


## Simple pixel effect that lights up each pixel in blue
## run with:
## fx.run '{"name": "pixel", "output": "1"}'
## make sure the output exists and is passed as a string
##
async def run(device, config):
    print("running pixel fx on", config['output'])
    output = device.outputs[config['output']]

    while True:
        for i in range(0, output.rgb_length()):
            output.rgb_set(i, (0, 0, 255))
            output.rgb_write()
            await asyncio.sleep_ms(100)
            output.rgb_set(i, (0, 0, 0))
