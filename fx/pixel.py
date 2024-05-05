import asyncio


async def run(output, data):
    print("running pixel fx", data)
    while True:
        for i in range(0, output.rgb_length()):
            output.rgb_set(i, (0, 0, 255))
            output.rgb_write()
            await asyncio.sleep_ms(100)
            output.rgb_set(i, (0, 0, 0))
