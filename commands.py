import sqlite3

# Permissions: "p000000" (default: "p100000")
# 1.   Chat
# 2.   Ban
# 3.   Can ban users
# 4-6. Other 
# 0 - false; 1 - true
# -------------------------------------------
# Codes: "c0"
# 0. quit

class Executor():
    
    commands = [
            "help", # print all commands
            "ban",  # ban user, onli users with p3 == 1 can use
            "quit"  # quit from server
            ]

    def __init__(self, login):
        self.conn = sqlite3.connect("databases/accounts")
        self.cursor = self.conn.cursor()
        self.login = login
    
    def checkPerms(self, perm):
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (self.login, ))
        perms = self.cursor.fetchone()
        return str(perms[3])[perm + 1]
    
    def checkCommand(self, command):
        command = command.partition(" ")[0]
        if command in self.commands:
            return True
        return False

    def makeCommand(self, command):
        commandCopy = command
        arguments = commandCopy.partition(" ")[2]
        command = command.partition(" ")[0]
        index = self.commands.index(command)
        match index:
            case 0:
                msg = str(self.commands)
                return msg
            case 1:
                if self.checkPerms(3) == "1":
                    self.cursor.execute("SELECT permissions FROM users WHERE name = ?", (arguments, ))
                    banUserPerms = self.cursor.fetchone()[0]
                    if banUserPerms == None:
                        msg = "User {} not found!".format(arguments)
                        return msg
                    list1 = list(banUserPerms)
                    list1[2] = '1'
                    str1 = "".join(list1)
                    self.cursor.execute("UPDATE users SET permissions = ? WHERE name = ?", (str1, arguments, ))
                    self.conn.commit()
                    msg = "User {} bunned success!".format(arguments)
                    print("User", arguments, "bunned by", self.login)
                    return msg
            case 2:
                return "c0"

    def stop(self):
        self.conn.close()
    
