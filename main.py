import asyncio

from game.core.protocol import GameProtocol


async def main():
    print("Starting MUD server")

    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()

    def factory():
        return GameProtocol()

    # Create server
    await loop.create_server(factory, '0.0.0.0', 4000)
    # Run forever
    await on_con_lost

asyncio.run(main())
