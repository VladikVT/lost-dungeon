from game.states.state import AbstractState


class LoginState(AbstractState):
    def __init__(self, player):
        self.step = 1
        player.sendln("Вы зарегистрированы? [д/н]")

    def process(self, command):
        if self.step == 1 and (command == "д" or command == "н"):
            self.step = 2

        return False