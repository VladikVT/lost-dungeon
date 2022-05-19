from datetime import date
from pony.orm import *


db = Database()


class User(db.Entity):
    _table_ = "users"

    # User ID
    id = PrimaryKey(int, auto=True)
    # User login
    login = Required(str, 64, unique=True)
    # User password
    password = Required(str, 64)
    # User permissions
    # bitmask, perms start from the second number from left
    # 1. can chat
    # 2. unban
    # 3-6. other
    permissions = Required(int, size=32, default=1110000)
    # User last online date
    last_online = Required(date)
    # User last IP
    last_ip = Optional(str, 15, nullable=True)


class Character(db.Entity):
    _table_ = "characters"

    # Character ID
    id = PrimaryKey(int, auto=True)
    # Associated user
    user = Set(User)
    # Character name
    name = Required(str, 64, unique=True)
    # Character health
    health = Required(int, size=32)
    # Character level
    level = Required(int, size=32, default=1)
    # Character experience
    experience = Optional(int, size=32)
    # Character race
    race = Required(str)
    # Character class
    kind = Required(str)
    # Character profession
    profession = Optional(str)
    # Character location (location ID)
    location = Required(int, size=32, default=0)
    # Character X position
    x = Optional(int, size=8, default=0)
    # Character Y position
    y = Optional(int, size=8, default=0)


class Skills(db.Entity):
    _table_ = "skills"

    # Associated character
    character = Set(Character)
    # Skill identifier
    skill = Required(str)
    # Skill level
    level = Required(int, size=32, default=0)
    # Skill experience
    experience = Required(int, size=32, default=0)
    # Skill experience modifier (can be given by race or temporary bonuses)
    modifier = Required(float)


class Inventory(db.Entity):
    _table = "inventory"

    # Identifier (for multiple items of same id)
    id = PrimaryKey(int, auto=True)
    # Associated character
    character = Set(Character)
    # Item identifier
    # All info about type and other characteristics gathered from .json file of this id
    item_id = Required(str)
    # Quality (1 - bad, 2 - decent, 3 - normal, 4 - great, 5 - master, 6 - mythical)
    quality = Required(int, size=3)
    # Durability
    durability = Required(int, default=100)
    # Max durability
    max_durability = Required(int, default=100)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)