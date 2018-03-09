import logging
import sys
import time

from ZO import ui
# TODO : This stuff will only work on a PC
from ZO.zero_one import ZeroOneException
from kbhit import KBHit

# TODO : Also put this is a PC wrapper
if 'debug' in sys.argv:
    sys.path.append('./pydev')
    from pydev import pydevd

    pydevd.settrace('localhost', port=51234, stdoutToServer=True, stderrToServer=True)

import time, threading
def foo():
    print(time.ctime())
    threading.Timer(0.2, foo).start()

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

    st = 0

    try:
        __ui = ui.get_ui_instance()
        command = None

        __ui.led_flash(ui.Led.LED_GREEN, 0.2)

        while command != ui.Commands.Quit:
            print('. ')
            time.sleep(0.2)
            command = __ui.get_command()

            if command == ui.Commands.Test:
                print('TEST')
                if st == 0:
                    __ui.led_on(ui.Led.LED_RED)

                if st == 1:
                    __ui.led_off(ui.Led.LED_RED)

                print(__ui)

                st = st + 1
                if st == 2:
                    st = 0

        __ui.shutdown()

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
