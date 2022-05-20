import sqlite3
from datetime import datetime
import logging

class LRform():
    def __init__(self):
        self.conn = sqlite3.connect("databases/accounts")
        self.cursor = self.conn.cursor() 

    def registration(self, login, nickname, password):
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (login, ))
        if self.cursor.fetchone() != None or login == "SERVER" or nickname == "SERVER":
            return False
        self.cursor.execute("INSERT INTO users (name, nick, password) VALUES (?, ?, ?)", (login, nickname, password, ))
        self.conn.commit()
        logging.info(f"Create new user: {login}, {nickname}")
        return True

    def login(self, login, password):
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (login, ))
        getUser = self.cursor.fetchone()
        if getUser != None:
            if password == getUser[2]:
                logging.info(f"User {login} login")
                return True, getUser[1]
            else:
                return False, None
        else:
            return False, None

    def stop(self):
        self.conn.close()
