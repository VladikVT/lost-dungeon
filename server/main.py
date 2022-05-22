import asyncio

from server import ServerProtocol as SP

host = "0.0.0.0"
port = 4000

async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: SP(),
        host, port)

    async with server:
        await server.serve_forever()


asyncio.run(main())
