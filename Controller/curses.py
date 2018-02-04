
import sys
import select

import time


def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False

def main():
    while True:
        print(heardEnter())
        time.sleep(0.2)


if __name__ == '__main__':
    main()