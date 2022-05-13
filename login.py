import sqlite3

class LRform():
    def __init__(self):
        self.conn = sqlite3.connect("databases/accounts")
        self.cursor = self.conn.cursor() 

    def registration(self, login, nickname, password):
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (login, ))
        if self.cursor.fetchone() != None:
            return False
        self.cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (login, nickname, password, ))
        self.conn.commit()
        print("Create new user: {}, {}, {}".format(login, nickname, password))
        return True

    def login(self, login, password):
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (login, ))
        getUser = self.cursor.fetchone()
        if getUser != None:
            if password == getUser[2]:
                print("User", login, "login")
                return True, getUser[1]
            else:
                return False, None
        else:
            return False, None
    
    def checkPerms(self, login, perm):
        # Permissions: "p000000"
        # 1.   Chat
        # 2.   Ban
        # 3-6. Other 
        # 0 - false; 1 - true
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (login, ))
        perms = self.cursor.fetchone()
        return str(perms[3])[perm + 1]

    def stop(self):
        self.conn.close()
