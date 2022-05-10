import socket
import threading

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

def handle(client):
    while True:
        try:
            index = clients.index(client)
            nickname = nicknames[index] + ": "
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(nickname, message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast("SERVER: ", '{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii').strip()
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is " + nickname)
        client.send('Connected to server!\n'.encode('ascii'))
        msg = nickname + " joined!\n"
        broadcast("SERVER: ", msg.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
