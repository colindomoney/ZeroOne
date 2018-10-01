# -*- coding: utf-8 -*-
import socket
# import os

port = 6999
host = socket.gethostname()

server = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen(5)
client, info = server.accept()

print("Opening socket...")
print("Listening...")

while True:
    datagram = client.recv(1024)
    if not datagram:
        break
    else:
        print("-" * 20)

        x = datagram.decode('utf-8')
        print(x)

        client.send(x.encode('utf-8'))

        if "DONE" == datagram.decode('utf-8'):
            break
print("-" * 20)
print("Shutting down...")
server.close()
print("Done")