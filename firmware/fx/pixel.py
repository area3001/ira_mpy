import asyncio


## Simple pixel effect that lights up each pixel in blue
## run with:
## fx.run '{"name": "pixel", "output": "1"}'
## make sure the output exists and is passed as a string
##
async def run(device, config):
    print("running pixel fx")
    outputs = device.output_config

    min_length = 5000
    for out_id in device.outputs:
        min_length = min(min_length, device.outputs[out_id].rgb_length())

    while True:
        for i in range(0, min_length):
            for out_id in device.outputs:
                device.outputs[out_id].rgb_set(i, (0, 0, 255))
                device.outputs[out_id].rgb_write()

            await asyncio.sleep_ms(100)

            for out_id in device.outputs:
                device.outputs[out_id].rgb_set(i, (0, 0, 0))
