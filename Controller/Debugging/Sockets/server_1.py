# -*- coding: utf-8 -*-
import socket
import os

SOCKET_HANDLE = "./zero_one_display_emulator.socket"

if os.path.exists(SOCKET_HANDLE):
    os.remove(SOCKET_HANDLE)

print("Opening socket...")
server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
server.bind(SOCKET_HANDLE)

print("Listening...")
while True:
    datagram = server.recv(1024)
    if not datagram:
        break
    else:
        print("-" * 20)
        print(datagram.decode('utf-8'))
        if "DONE" == datagram.decode('utf-8'):
            break
print("-" * 20)
print("Shutting down...")
server.close()
os.remove(SOCKET_HANDLE)
print("Done")