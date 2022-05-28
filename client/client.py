import asyncio
import json


class ClientProtocol(asyncio.Protocol):
    
    jsonTempl = {
            "code": 0,
            "state": 0,
            "message": "message"
            }

    def __init__(self, on_con_lost, loop):
        self.on_con_lost = on_con_lost
        self.loop = loop
        self.encoding = "utf-8"
        self.state = 0
        self.working = True
        self.debugMode = False

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        print("The server closed the connection")
        self.working = False
        self.on_con_lost.set_result(True)

    def data_received(self, data):
        try: 
            message = json.loads(data.decode(self.encoding))
            if message["code"] == 0:
                self.state = message["state"]
            if self.debugMode:
                print(f"{message['sender']} >>> {message}")
            else:
                print(f"{message['sender']} >>> {message['message']}")
        except Exception as exc:
            print(f"Listener === {exc}")
            print("Stop connection")
            self.working = False
            self.transport.close()

    async def clientCmdHandler (self):
        while self.working:
            cmd = await self.loop.run_in_executor(None, input, "")
            if cmd.strip() != "":
                self.send(0, cmd)
    
    def send(self, code, msg):
        self.jsonTempl["code"] = code
        self.jsonTempl["state"] = self.state
        self.jsonTempl["message"] = msg
        data = json.dumps(self.jsonTempl)
        self.transport.write(data.encode(self.encoding))
