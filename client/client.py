import asyncio


class ClientProtocol(asyncio.Protocol):
    def __init__(self, on_con_lost, loop):
        self.on_con_lost = on_con_lost
        self.loop = loop
        self.encoding = "utf-8"

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        data = data.decode(self.encoding)
        print(f"SERVER >>> {data}")

    def connection_lost(self, exc):
        print("The server closed the connection")
        self.on_con_lost.set_result(True)

    def send(self, data):
        self.transport.write(data.encode(self.encoding))
        
    async def clientCmdHandler (self, loop):
        while True:
            cmd = await loop.run_in_executor(None, input, "YOU >>> ")
            cmd.strip()

            if cmd != "":
                self.send(cmd)

            if cmd == "quit":
                break


