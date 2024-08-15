import asyncio

def clear(string):
    for i in range(0, string.rgb_length()):
        string.rgb_set(i, (0,0,0))


## Simple pixel effect that lights up each pixel in blue
## run with:
## fx.run '{"name": "knightrider", "output": "1"}'
## make sure the output exists and is passed as a string
##
async def run(device, config):
    print("running knightrider fx on", config['output'])
    output = device.outputs[config['output']]

    pos = 0
    bar_len = 3

    while True:
        for i in range(0, output.rgb_length()-bar_len):
            clear(output)
            for j in range(0, bar_len):
                output.rgb_set(i+j, (255,0,0))
            output.rgb_write()
            await asyncio.sleep_ms(10)
        for i in range(output.rgb_length()-bar_len-1,0-1,-1):
            clear(output)
            for j in range(bar_len):
                output.rgb_set(i+j, (255,0,0))
            output.rgb_write()
            await asyncio.sleep_ms(20)
        await asyncio.sleep_ms(500)