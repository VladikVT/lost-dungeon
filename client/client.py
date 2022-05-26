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
        self.working = False
        self.debugMode = False

    def run(self):
        self.working = True
        self.listenThread = Thread(target = self.Listener)
        self.listenThread.start()
        self.handle()

    def Listener(self):
        try:
            while True:
                if not self.working:
                    return
                data = self.sock.recv(1024).decode(self.encoding)
                if not data: 
                    break
                data = json.loads(data)
                if data["code"] == 0:
                    self.state = data["state"]
                if self.debugMode:
                    print(f"SERVER >>> {data}")
                else:
                    print(f"SERVER >>> {data['message']}")
        except Exception as exc:
            print(f"Listener === {exc}")
        finally:
            print("Stop connection")
            self.working = False
            self.sock.close()

    def handle(self):
        try:
            while True:
                msg = input()
                if not self.working:
                    return
                msg.strip()
                if msg == "": 
                    continue
                self.send(0, msg)
        except Exception as exc:
            print(f"handle === {exc}")
        finally:
            self.working = False
            self.sock.close()
    
    def send(self, code, msg):
        self.jsonTempl["code"] = code
        self.jsonTempl["state"] = self.state
        self.jsonTempl["message"] = msg
        data = json.dumps(self.jsonTempl)
        self.sock.send(data.encode(self.encoding))
