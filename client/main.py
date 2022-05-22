import asyncio

from client import ClientProtocol as CP

host = "127.0.0.1"
port = 4000

async def main():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()

    client = CP(on_con_lost, loop)

    transport, protocol = await loop.create_connection(
        lambda: client,
        host, port)
    
    await client.clientCmdHandler(loop)

asyncio.run(main())
