import logging
import os
import sys
import time

from ZO import ui, display
# TODO : This stuff will only work on a PC
from ZO.ui import Button
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
    tick = 0;

    try:
        _ui = ui.get_ui_instance()
        command = None

        # _ui.led_on(ui.Led.LED_RED)
        # _ui.led_flash(ui.Led.LED_RED, 0.2)
        _ui.led_flash(ui.Led.LED_RED, 0.1)

        this_directory = os.path.dirname(os.path.realpath(__file__))
        binary_path = os.path.join(this_directory, "fadecandy/bin/fcserver-osx")
        config_path = os.path.join(this_directory, "fadecandy/bin/test-rig_config.json")

        fcserver = display.FCServer(binary_path, config_path)
        print(fcserver)

        while command != ui.Commands.Quit:
            print('. ')
            time.sleep(0.1)
            command = _ui.get_command()

            button = _ui.get_button()

            if button != None:
                if button == Button.BUTTON_1:
                    print('BUTTON_1')
                elif button == Button.BUTTON_2:
                    print('BUTTON_2')
                elif button == Button.BUTTON_3:
                    print('BUTTON_3')
                    raise ZeroOneException('Critical failure - user bored', 4)

            # if _ui.test_button(Button.BUTTON_3):
            #     _ui.led_on(ui.Led.LED_AMBER)
            # else:
            #     _ui.led_off(ui.Led.LED_AMBER)

            # tick = tick+1
            # if tick > 20:
            #     print('Queue:', _ui.get_button())
            #     tick = 0

            if command == ui.Commands.Test:
                print('TEST')

                if st == 0:
                    pass

                if st == 1:
                    pass

                print(_ui)

                st = st + 1
                if st == 2:
                    st = 0

        _ui.shutdown()

        # Flush the keyboard here
        # TODO : is this even needed anymore
        kb = KBHit()
        kb.flush()

    except KeyboardInterrupt as ex:
        print("Aborted")

    except ZeroOneException as ex:
        print("\n>>> EXCEPTION : {} <<<\n".format(ex.message))
        log.error(ex.message, exc_info=True)
        _ui.display_exception(ex.error_code)

    finally:
        _ui.shutdown()
        destroy_logging()
        print('Done!')


if __name__ == "__main__":
    main()
