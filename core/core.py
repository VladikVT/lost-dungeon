import asyncio
import json

from game.entities.player.player import Player


class CoreProtocol(asyncio.Protocol):
    
    jsonTempl = {
            "code": 0,
            "state": 0,
            "message": "message"
            }

    def connection_made(self, transport):
        self.peername = transport.get_extra_info("peername")
        print(f"Connection from {self.peername}")
        self.transport = transport
        self.encoding = "utf-8"
        self.player = Player(transport)

    def data_received(self, data):
        try:
            data = data.decode(self.encoding)
            cmd = json.loads(data)["message"]
            self.player.cmdDetector(cmd)
            print(f"{self.peername} >>> {data}")
        except Exception as exp:
            print(f"ERROR[RECV] >>> {exp}")

    def send(self, code, msg):
        self.jsonTempl["code"] = code
        self.jsonTempl["message"] = msg
        data = json.dumps(self.jsonTempl)
        self.transport.write(data.encode(self.encoding))


