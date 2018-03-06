import logging
import time
from ZO import ui
import sys, os, io

# TODO : This stuff will only work on a PC
from ZO.zero_one import ZeroOneException
from kbhit import KBHit

# TODO : Also put this is a PC wrapper
if 'debug' in sys.argv:
    sys.path.append('./pydev')
    from pydev import pydevd

    pydevd.settrace('localhost', port=51234, stdoutToServer=True, stderrToServer=True)


def main():
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

    # Start the main program here

    print('Testing UI ...')
    setup_logging()

    try:

        __ui = ui.get_ui_instance()
        command = None

        while command != ui.Commands.Quit:
            print('. ')
            time.sleep(0.2)
            command = __ui.get_command()

            if command == ui.Commands.Test:
                print('TEST')
                __ui.led_on(ui.UIBase.Led.LED_RED)

        # Flush the keyboard here
        # TODO : is this even needed anymore
        kb = KBHit()
        kb.flush()

    except ZeroOneException as ex:
        print("\n>>> EXCEPTION : {} <<<\n".format(ex.message))
        log.error(ex.message, exc_info=True)
        pass

    destroy_logging()
    print('Done!')


if __name__ == "__main__":
    main()
