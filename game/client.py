from asyncio import Transport


class Client:
    def __init__(self, transport: Transport):
        self.transport = transport
        self.encoding = "utf-8"

    def setEncoding(self, encoding):
        self.encoding = encoding

    def write(self, msg):
        if type(msg) == str:
            msg = msg.encode(self.encoding)
        self.transport.write(msg)

    def writeln(self, msg):
        self.write(msg + "\n")

    def kick(self):
        self.transport.abort()
