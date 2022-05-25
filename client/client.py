from threading import Thread
from socket import *
import json


class ClientProtocol():
    
    jsonTempl = {
            "code": 0,
            "state": 0,
            "message": "message"
            }

    def __init__(self, sock):
        self.sock = sock
        self.encoding = "utf-8"
        self.state = 0
        self.mainHandleOn = True

    def run(self):
        self.listenThread = Thread(target = self.Listener)
        self.listenThread.start()
        self.handle()

    def Listener(self):
        try:
            while True:
                data = self.sock.recv(1024).decode(self.encoding)
                if not data: break
                data = json.loads(data)
                if data["code"] == 0:
                    self.state = data["state"]
                    self.stateMachine()
                print(f"\nSERVER >>> {data}")
        except Exception as exc:
            print(f"Listener === {exc}")
        finally:
            print("Stop connection")
            self.sock.close()

    def handle(self):
        try:
            while True:
                if self.mainHandleOn:
                    msg = input("YOU >>> ")
                    msg.strip()
                    if msg == "": continue
                    self.send(0, msg)
        except Exception as exc:
            print(f"handle === {exc}")
        finally:
            self.sock.close()
    
    def send(self, code, msg):
        self.jsonTempl["code"] = code
        self.jsonTempl["state"] = self.state
        self.jsonTempl["message"] = msg
        data = json.dumps(self.jsonTempl)
        self.sock.send(data.encode(self.encoding))

    def stateMachine(self):
        match self.state:
            case 2:
                self.mainHandleOn = False
                login = input("Login: ")
                password = input("Password: ")
                self.send(0, f"{login}*{password}")
                self.mainHandleOn = True
            case 3:
                self.mainHandleOn = False
                login = input("Login: ")
                nick = input("Nickname: ")
                password = input("Password: ")
                self.send(0, f"{login}*{nick}*{password}")
                self.mainHandleOn = True
