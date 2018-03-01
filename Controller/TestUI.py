import time
from ZO import ZeroOne, ui
import sys, os, io
from kbhit import KBHit


if 'debug' in sys.argv:
    sys.path.append('./pydev')
    from pydev import pydevd
    pydevd.settrace('localhost', port=51234, stdoutToServer=True, stderrToServer=True)

def main():
    print('Testing UI ...')

    __ui = ui.get_ui_instance()
    command = None

    while command != ui.Commands.Quit:
        print('. ')
        time.sleep(0.1)
        command = __ui.get_command()

    # Flush the keyboard here
    kb = KBHit()
    kb.flush()

    print('Done!')

if __name__ == "__main__":
    main()