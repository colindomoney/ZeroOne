import time, threading
from pynput.keyboard import Key, Listener
from getkey import getkey, keys

import sys
sys.path.append('./pydev')
# sys.path.append('./pydev.egg')
from pydev import pydevd
pydevd.settrace('localhost', port=51234, stdoutToServer=True, stderrToServer=True)

# def toggle_led():
#     print(". ")
#     global timer
#     timer = threading.Timer(1, toggle_led)
#     timer.start()


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

def main():
    key = getkey()
    buffer = ''
    if key == keys.UP:
        pass
    elif key == keys.DOWN:
        pass
    else:  # Handle text characters
        buffer += key
        print(buffer)

if __name__ == "__main__":
    main()