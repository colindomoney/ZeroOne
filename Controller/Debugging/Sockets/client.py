# -*- coding: utf-8 -*-
import socket
import os

port = 6999
host = socket.gethostname()

client = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))

print("Ready.")
print("Ctrl-C to quit.")
print("Sending 'DONE' shuts down the server and quits.")

while True:
    try:
        x = input("> ")

        if "" != x:
            print("SEND:", x)
            client.send(x.encode('utf-8'))

            datagram = client.recv(1024)
            if not datagram:
                break
            else:
                print("-" * 20)

                x = datagram.decode('utf-8')
                print(x)

            if "DONE" == x:
                print("Shutting down.")
                break
    except KeyboardInterrupt as k:
        print("Shutting down.")
        client.close()
        break

# else:
#     print("Couldn't Connect!")

print("Done")
