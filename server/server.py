import asyncio


class ServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        print(f"Connection from {peername}")
        self.transport = transport
        self.encoding = "utf-8"

    def data_received(self, data):
        self.send(data.decode(self.encoding))

    def send(self, data):
        self.transport.write(data.encode(self.encoding))

    def kick(self):
        self.transport.close()




