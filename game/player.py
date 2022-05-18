from game.client import Client

cmds = ["quit", "shit"]


class Player:

    def __init__(self, transport):
        self.client = Client(transport)
        self.encoding = self.client.encoding

    def kick(self):
        self.client.kick()

    def send(self, message):
        self.client.writeln(message)

    def process(self, command):
        if command in cmds:
            self.send("There is such command")