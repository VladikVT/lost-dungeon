import asyncio
import json

class Player:

    jsonTempl = {
            "code": 0,
            "state": 0,
            "message": "message"
            }

    def __init__(self, transport):
        self.transport = transport
        self.encoding = "utf-8"
        self.state = 0
        self.stateMachine()

    def cmdDetector(self, cmd):
        cmd.strip()
        if cmd[0] == "!":
            print(cmd)
            return
        
        command = cmd.partition(" ")[0]
        argument = cmd.partition(" ")[2]

        self.stateMachine(command)

        if self.state != 4:
            return

        match command:
            case "quit":
                self.kick()
            case "ping":
                self.send(0, "pong")

    def stateMachine(self, command = None):
        match self.state:
            case 0:
                self.state = 1
                self.send(0, "Has account [y/n] ")
            case 1 if command in "yes":
                self.state = 2
                self.send(0, "")
            case 1 if command in "not":
                self.state = 3
                self.send(0, "")
            case 1:
                self.send(0, "Has account [y/n] ")
            case 3:
                self.state = 4
                self.send(0, "Success login")

    def send(self, code, msg):
        self.jsonTempl["code"] = code
        self.jsonTempl["state"] = self.state
        self.jsonTempl["message"] = msg
        data = json.dumps(self.jsonTempl)
        self.transport.write(data.encode(self.encoding))

    def kick(self):
        self.transport.close()
