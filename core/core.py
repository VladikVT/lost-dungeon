import asyncio

from game.entities.player.player import Player


class CoreProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.peername = transport.get_extra_info("peername")
        print(f"Connection from {self.peername}")
        self.transport = transport
        self.encoding = "utf-8"
        self.player = Player(transport)

    def data_received(self, data):
        cmd = data.decode(self.encoding)
        self.player.cmdDetector(cmd)
        print(f"{self.peername} >>> {data.decode(self.encoding)}")

    def send(self, data):
        self.transport.write(data.encode(self.encoding))


