import asyncio
import json
from pony.orm import *

from databases import User, Character

clients = []

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
        if cmd[0] == "!" and self.state == 6:
            for i in clients:
                self.send(1, cmd, i)
            return
        
        command = cmd.partition(" ")[0]
        argument = cmd.partition(" ")[2]

        self.stateMachine(command)

        if self.state != 6:
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
                self.send(0, "Login: ")
            case 1 if command in "not":
                self.state = 4
                self.send(0, "Login: ")
            case 1:
                self.send(0, "Has account [y/n] ")
            case 2:
                self.login = command
                self.state = 3
                self.send(0, "Password: ")
            case 3:
                self.password = command
                if not self.checkUserPass(self.login, self.password):
                    self.state = 0
                    self.send(0, "Login or password incorrect!")
                    self.stateMachine()
                    return
                self.state = 6
                self.send(0, "Success login!")
                clients.append(self.transport)
            case 4:
                self.login = command
                self.state = 5
                self.send(0, "Password: ")
            case 5:
                self.password = command
                if self.checkUser(self.login):
                    self.state = 0
                    self.send(0, "This login already used!")
                    self.stateMachine()
                    return
                self.send(0, "Success registration!")
                print(f"New user: {self.login}, {self.password}")
                self.createUser(self.login, self.password)
                self.state = 6
                clients.append(self.transport)
                self.send(0, "")

    def send(self, code, msg, client = None):
        self.jsonTempl["code"] = code
        self.jsonTempl["state"] = self.state
        self.jsonTempl["message"] = msg
        data = json.dumps(self.jsonTempl)
        if client:
            client.write(data.encode(self.encoding))
        else:
            self.transport.write(data.encode(self.encoding))

    def kick(self):
        self.transport.close()

    @db_session
    def checkUser(self, login):
        if User.get(login=login):
            return True
        return False
    
    @db_session
    def checkUserPass(self, login, password):
        user = User.get(login=login)
        if user and user.password == password:
            return True
        return False

    @db_session
    def createUser(self, login, password):
        User(login=login, password=password)
        commit()


