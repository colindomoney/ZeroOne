import time

from ZO import ZeroOne, ui
import sys, os, io


def main():
    print('Testing UI ...')

    __ui = ui.get_ui_instance()
    print(__ui)

    time.sleep(1)

    __ui.test()

    time.sleep(5)
    print('Done!')

if __name__ == "__main__":
    main()