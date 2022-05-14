import socket
import threading

from login import LRform
from commands import Executor

# Connection Data
host = '127.0.0.1'
port = 4000

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(nickname, message):
    msg = nickname + message.decode('ascii')
    for client in clients:
        client.send(msg.encode('ascii'))

def handle(client, login):
    cmd = Executor(login)
    while True:
        try:
            index = clients.index(client)
            nickname = nicknames[index] + ": "
            # Broadcasting Messages
            message = client.recv(1024).decode('ascii').strip()
            if message == "":
                continue
            if message[0] == "!":
                if cmd.checkPerms(0) == "1":
                    message = str(message[1:]) + "\n"
                    broadcast(nickname, message.encode('ascii'))
                else:
                    client.send('You not have permissions to chat\n'.encode('ascii'))
            else:
                if not cmd.checkCommand(message):
                    client.send('Not correct command! For see command list write "help"\n'.encode('ascii'))
                else:
                    msg = cmd.makeCommand(message) + "\n"
                    if msg[0] == "c":
                        match msg[1]:
                            case "0": 1 / 0 # Error for quit =)
                    client.send(msg.encode('ascii'))
        except Exception as err:
            print(err)
            # Removing And Closing Clients
            print("{} disconnected!".format(client.getpeername()))
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast("SERVER: ", '{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            cmd.stop()
            break

# Receiving / Listening Function
def receive():
    while True:
        form = LRform()
        cmd = None
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        
        # Has account or not
        successLogin = False
        hasAcc = ""
        login = ""
        nickname = ""
        password = ""
        try:
            while True:
                client.send('Has account? [y/n] '.encode('ascii'))
                hasAcc = client.recv(1024).decode('ascii').strip()
                if hasAcc in "yes" or hasAcc in "not":
                    break
            while not successLogin:
                if hasAcc in "not":
                    client.send('Your login: '.encode('ascii'))
                    login = client.recv(1024).decode('ascii').strip()
                    client.send('Your nickname: '.encode('ascii'))
                    nickname = client.recv(1024).decode('ascii').strip()
                    client.send('Your password: '.encode('ascii'))
                    password = client.recv(1024).decode('ascii').strip()
                    successLogin = form.registration(login, nickname, password)
                    if not successLogin:
                        msg = "Login {} already used\n".format(login)
                        client.send(msg.encode('ascii'))
                elif hasAcc in "yes":
                    client.send('Your login: '.encode('ascii'))
                    login = client.recv(1024).decode('ascii').strip()
                    client.send('Your password: '.encode('ascii'))
                    password = client.recv(1024).decode('ascii').strip()
                    successLogin, nickname = form.login(login, password)
                    if not successLogin:
                        client.send('Not correct login or password\n'.encode('ascii'))
            cmd = Executor(login)
            if cmd.checkPerms(1) == "1":
                client.send('This account has banned\n'.encode('ascii'))
                print("{} disconnected!".format(client.getpeername()))
                form.stop()
                client.close()
                continue
        except Exception as err:
            print(err)
            print("{} disconnected!".format(client.getpeername()))
            form.stop()
            client.close()
            continue

        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is", nickname)
        client.send('Connected to server!\n'.encode('ascii'))
        msg = str(nickname) + " joined!\n"
        broadcast("SERVER: ", msg.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client, login, ))
        thread.start()
        
        form.stop()

if __name__ == "__main__":
    print("---=== SERVER START ===---")
    receive()
