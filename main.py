import asyncio
import network
from ira import Ira

async def main():
    import network
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('area3001', 'hackerspace')
        while not sta_if.isconnected():
            pass
    
    print('network config:', sta_if.ifconfig())

    i = Ira('my_id', 'my_name', 'ira', '2024')
    await i.listen()
    print('listening to ira messages')

asyncio.run(main())