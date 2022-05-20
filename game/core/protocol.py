import asyncio

from game.player.player import Player


class GameProtocol(asyncio.Protocol):
    def __init__(self):
        self.player = None

    def connection_made(self, transport):
        self.player = Player(transport)

    def data_received(self, data):
        try:
            message = data.decode(self.player.encoding).strip()
        except UnicodeDecodeError:
            message = None

        if message:
            self.player.process(message)
