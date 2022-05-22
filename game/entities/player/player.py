import asyncio

class Player:
    def __init__(self, transport):
        self.transport = transport
        self.encoding = "utf-8"
        self.state = 0
        self.stateMachine()

    def cmdDetector(self, cmd):
        if cmd[0] == "!":
            print(cmd)
            return
        
        command = cmd.partition(" ")[0]
        argument = cmd.partition(" ")[2]

        self.stateMachine(command)

        if self.state != 3:
            return

        match command:
            case "quit":
                self.kick()
            case "ping":
                self.send("pong")

    def stateMachine(self, command = None):
        match self.state:
            case 0:
                self.state = 1
                self.send("You have account? [y/n] ")
            case 1 if command in "yes":
                self.state = 2
                self.send("Login: ")
            case 1 if command in "not":
                self.state = 3
                self.send("Login: ")
            case 1:
                self.send("You have account? [y/n] ")
            case 2:
                self.state = 4
                self.send("Password: ")

    def send(self, data):
        self.transport.write(data.encode(self.encoding))

    def kick(self):
        self.transport.close()
