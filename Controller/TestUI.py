import time
from ZO import ZeroOne, ui
import sys, os, io

# TODO : This stuff will only work on a PC
from kbhit import KBHit

# TODO : Also put this is a PC wrapper
if 'debug' in sys.argv:
    sys.path.append('./pydev')
    from pydev import pydevd
    pydevd.settrace('localhost', port=51234, stdoutToServer=True, stderrToServer=True)

def main():
    print('Testing UI ...')

    # TODO : Check if we get an instance and fail the whole programme if we don't
    __ui = ui.get_ui_instance()
    command = None

    while command != ui.Commands.Quit:
        print('. ')
        time.sleep(0.2)
        command = __ui.get_command()

        if command == ui.Commands.Test:
            print('TEST')

    # Flush the keyboard here
    # TODO : is this even needed anymore
    kb = KBHit()
    kb.flush()

    print('Done!')

if __name__ == "__main__":
    main()