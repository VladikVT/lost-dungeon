from datetime import date
from pony.orm import *


db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Required(str, 64, unique=True)
    password = Required(str, 64)
    permissions = Required(int, size=32, default=1110000)
    # Permissions
    # bitmask, perms start from the second number from left
    # 1. can chat
    # 2. unban
    # 3-6. other
    last_online = Required(date)
    last_ip = Optional(str, 15, default="255.255.255.255")
    player = Set('Player')
    state = Required(int, size=32, default=0)


class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Set(User)
    name = Required(str, 64, unique=True)
    HP = Required(int, size=32)
    level = Required(int, size=32, default=1)
    XP = Optional(int, size=32)
    skills = Required(Json)
    race = Required(str)
    profession = Required(str)  # player class
    inventory = Set('Inventory')
    location = Required(int, size=32, default=0)
    posX = Optional(int, size=8, default=0)
    posY = Optional(int, size=8, default=0)
    state = Required(int, size=32, default=0)


class Inventory(db.Entity):
    id = PrimaryKey(int, auto=True)
    player = Set(Player)
    items = Required(Json)
    equipment = Required(Json)
    size = Required(int, size=8, default=16)
    items_count = Required(int, size=8, default=0)



db.generate_mapping()
