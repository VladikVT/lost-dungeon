from game.core.client import Client
from game.states.login import LoginState
from game.core.state import StateMachine

cmds = ["quit", "shit"]


class Player:

    def __init__(self, game, transport):
        self.game = game

        self.client = Client(transport)
        self.encoding = self.client.encoding
        self.state = StateMachine(self)

        self.state.move(LoginState)

    def kick(self):
        self.client.kick()

    def sendln(self, message):
        self.client.writeln(message)

    def send(self, message):
        self.client.write(message)

    def process(self, command):
        suppress = self.state.process(command)

        if not suppress:
            if command in cmds:
                self.sendln("There is such command")