import asyncio


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colors are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


async def run(output, data):
    print("running rainbow fx", data)
    while True:
        for j in range(255):
            for i in range(output.rgb_length()):
                rc_index = (i * 256 // output.rgb_length()) + j
                # print(rc_index)

                output.rgb_set(i, wheel(rc_index & 255))

            output.rgb_write()
            await asyncio.sleep_ms(20)
        await asyncio.sleep_ms(20)