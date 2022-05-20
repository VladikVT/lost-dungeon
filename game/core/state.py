class StateMachine:

    def __init__(self, player):
        self.state = None
        self.player = player

    def move(self, state):
        self.state = state
        self.state(self.player)

    def process(self, command):
        return self.state.process(self.state, command)
