import asyncio
import json
from pony.orm import *
from datetime import datetime

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
        
        command = cmd.partition(" ")[0]
        argument = cmd.partition(" ")[2]
        
        if self.state != 10:
            self.stateMachine(command)
            return

        if cmd[0] == "!":
            for i in clients:
                self.send(1, cmd, i)
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
                if not self.checkUserPass():
                    self.state = 2
                    self.send(0, "Login or password incorrect!\nLogin: ")
                    return
                self.state = 10
                self.updateLoginData()
                clients.append(self.transport)
                self.send(0, "Success login!")
            case 4:
                self.login = command
                if self.checkUser():
                    self.send(0, "This login already used!\nLogin: ")
                    return
                self.state = 5
                self.send(0, "Password: ")
            case 5:
                self.password = command
                self.state = 6
                self.send(0, "Character name: ")
            case 6:
                self.charName = command
                if self.checkCharacter():
                    self.send(0, "This name already used!\nCharacter name: ")
                    return
                self.state = 7
                self.send(0, "Choose race:\n1. Human\n2. Elf\n3. Dwarf\n(Write class number)")
            case 7:
                match command:
                    case "1" | "human":
                        self.race = "human"
                    case "2" | "elf":
                        self.race = "elf"
                    case "3" | "dwarf":
                        self.race = "dwarf"
                    case _:
                        self.state = 6
                        self.stateMachine(self.charName)
                        return
                self.state = 8
                self.send(0, "Choose class:\n1. Wizard\n2. Ranger\n3. Warrior\n(Write class number)")
            case 8:
                match command:
                    case "1" | "wizard":
                        self.kind = "wizard"
                    case "2" | "ranger":
                        self.kind = "ranger"
                    case "3" | "warrior":
                        self.kind = "warrior"
                    case _:
                        self.state = 7
                        self.stateMachine(self.race)
                        return
                self.state = 9
                self.send(0, "Choose profession:\n1. Blacksmith\n2. Alchemist\n3. Baker\n(Write profession number)")
            case 9:
                match command:
                    case "1" | "blacksmith":
                        self.profession = "blacksmith"
                    case "2" | "alchemist":
                        self.profession = "alchemist"
                    case "3" | "baker":
                        self.profession = "baker"
                    case _:
                        self.state = 8
                        self.stateMachine(self.kind)
                        return
                self.state = 10
                self.createUser()
                self.createCharacter()
                self.updateLoginData()
                self.state = 10
                clients.append(self.transport)
                print(f"New user: {self.login}, {self.password}")
                self.send(0, "Success registration!")

    def send(self, code, msg, client = None):
        self.jsonTempl["code"] = code
        self.jsonTempl["state"] = self.state
        self.jsonTempl["message"] = msg
        data = json.dumps(self.jsonTempl)
        if client:
            try:
                client.write(data.encode(self.encoding))
            except:
                clients.remove(client)
        else:
            self.transport.write(data.encode(self.encoding))

    def kick(self):
        self.transport.close()
    
    @db_session
    def updateLoginData(self):
        user = User.get(login = self.login)
        user.last_online = datetime.now()
        user.last_ip = self.transport.get_extra_info("socket").getpeername()[0]
        commit()

    @db_session
    def checkUser(self):
        if User.get(login = self.login):
            return True
        return False

    @db_session
    def checkCharacter(self):
        if Character.get(name = self.charName):
            return True
        return False
    
    @db_session
    def checkUserPass(self):
        user = User.get(login = self.login)
        if user and user.password == self.password:
            return True
        return False

    @db_session
    def createUser(self):
        User(login = self.login, password = self.password)
        commit()

    @db_session
    def createCharacter(self):
        Character(name = self.charName, race = self.race, kind = self.kind, profession = self.profession, user = User.get(login = self.login))
        commit()


