import sys
import threading
import time
from enum import Enum

from getkey import getkey, keys
from pynput.keyboard import Key, Listener


# import sys
# sys.path.append('./pydev')
# from pydev import pydevd
# pydevd.settrace('localhost', port=51234, stdoutToServer=True, stderrToServer=True)

def toggle_led():
    print(". ")
    global timer
    timer = threading.Timer(1, toggle_led)
    timer.start()


def main1():
    # toggle_led()

    try:
        print('Running main')
        cnt = 0

        while True:
            time.sleep(0.2)
            print('x')
            time.sleep(0.2)

            cnt = cnt + 1
            # if (cnt > 4):
            #     timer.cancel()

    except KeyboardInterrupt:
        print("Exiting")
        # timer.cancel()

def main2():
    def on_press(key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(key):
        print('{0} released'.format(
            key))
        if key == Key.esc:
            # Stop listener
            return False

    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

def main3():
    key = getkey()
    buffer = ''
    if key == keys.UP:
        pass
    elif key == keys.DOWN:
        pass
    else:  # Handle text characters
        buffer += key
        print(buffer)

def main():
    print('in main()')

    class Keys(Enum):
        KEY1 = 'q'
        KEY2 = 'w'
        KEY3 = 'e'

        @classmethod
        def contains(cls, key):
            return any(key == item.value for item in cls)

        @classmethod
        def byvalue(cls, val):
            for item in cls:
                if item.value == val:
                    return item.name
            return None


    v1 = ['q' == item.value for item in Keys]

    print(v1)

import logging

def main_logging():

    def setup_logging():
        print("setup_logging")

        logging.basicConfig(
            format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
            handlers=[
                logging.FileHandler("./zero_one.log"),
                logging.StreamHandler(sys.stdout)
            ])

        global log
        log = logging.getLogger('zero_one')
        log.setLevel(logging.INFO)

    def destroy_logging():
        print("destroy_logging")

    setup_logging()

    log.info('info')

    destroy_logging()

if __name__ == "__main__":
    toggle_led()