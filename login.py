import sqlite3

class LRform():
    def __init__(self):
        self.conn = sqlite3.connect("databases/accounts")
        self.cursor = self.conn.cursor() 

    def registration(self, name):
        name.rstrip()
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        print(self.cursor.fetchone())

    def stop(self):
        self.conn.close()
