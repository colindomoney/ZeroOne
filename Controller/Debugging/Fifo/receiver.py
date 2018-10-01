import os
import sys

path = "./my_program.fifo"
fifo = open(path, "r")
for line in fifo:
    print("Received: " + line)
fifo.close()
