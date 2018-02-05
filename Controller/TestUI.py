import time
from ZO import ZeroOne, ui
import sys, os, io
import getch

if 'debug' in sys.argv:
    sys.path.append('./pydev')
    from pydev import pydevd
    pydevd.settrace('localhost', port=51234, stdoutToServer=True, stderrToServer=True)

def main():
    print('Testing UI ...')

    __ui = ui.get_ui_instance()
    command = None

    while command != ui.Commands.Quit:
        time.sleep(0.1)
        command = __ui.get_command()
        print('. ')

    print('Done!')

if __name__ == "__main__":
    main()