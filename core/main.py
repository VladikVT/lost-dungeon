import asyncio

from core.core import CoreProtocol as CoreP

host = "0.0.0.0"
port = 4000

async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: CoreP(),
        host, port)

    async with server:
        await server.serve_forever()



