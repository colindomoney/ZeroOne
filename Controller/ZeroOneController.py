import getopt, json
import time, logging, os, sys
from pprint import pprint

from ZO import ui, display
from ZO.ui import Button
from ZO.zero_one import ZeroOneException
from kbhit import KBHit


def setup_logging():
    print("setup_logging")

    logging.basicConfig(
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler("./ZeroOneController.log"),
            logging.StreamHandler(sys.stdout),
        ],
        level=logging.INFO)

def destroy_logging():
    print("destroy_logging")
    logging.shutdown()

# numLEDs = 591
# client = opc.Client('localhost:7890')
#
# black = [ (0, 0, 0) ] * numLEDs
# white = [ (0, 255, 0) ] * numLEDs
#
# if client.can_connect():
#     print("Connected to server")
# else:
#     print("FAILED to connect to server")
#     exit(1)
#
# try:
#
#     while True:
#         z = ZO.ZeroOne()
#
#         print('. ')
#         client.put_pixels(white)
#         time.sleep(0.25)
#         client.put_pixels(black)
#         time.sleep(0.25)
#
# except KeyboardInterrupt:
#     print('Exiting ...')
#     client.put_pixels(black)

def parse_config():
    with open('config.json', 'r') as f:
        config = json.load(f)

    secret_key = config['DEFAULT']['SECRET_KEY']  # 'secret-key-of-myapp'
    ci_hook_url = config['CI']['HOOK_URL']  # 'web-hooking-url-from-ci-service'

# TODO : This is what the main code needs to:
# 1. Read the config file
# 2. Identify the hardware platform (use the Pi test, look for a hidden file)
# 3. Enable the buttons and LEDs
# 4. Enable the display driver(s)

# Options:
# 1. Debug mode for I/O ie. buttons and LEDs
# 2. Debug mode to blit to screen

def main(argv):
    print('ZeroOneController running ...')

    # Set up the logging
    setup_logging()
    logging.info('ZeroOneController running ...')

    # Get the UI instance
    app_ui = ui.get_ui_instance()
    command = None

    # Read the config file
    config_file = './config.ini'
    try:
        opts, args = getopt.getopt(argv, "hc:", ["config="])
    except getopt.GetoptError:
        print('ZeroOneController.py --config <configfile>')
        raise ZeroOneException()

    for opt, arg in opts:
        if opt in ('-c', '--config'):
            config_file = arg

    # Test the config file exists
    print('Using config from', config_file)
    if os.path.exists(config_file) == False:
        raise ZeroOneException("Config file {0} does not exist".format(config_file))
    else:
        # TODO : This should catch the json.decoder.JSONDecodeError exception
        with open(config_file) as cf:
            data = json.load(cf)

            config_fadecandy = data['Fadecandy']
            pprint(config_fadecandy)

            config_emulator = data['DisplayEmulator']
            pprint(config_emulator)

            this_directory = os.path.dirname(os.path.realpath(__file__))

    # Now create a display object
    app_display = display.Display(config_fadecandy, config_emulator)
    print(app_display)
    app_display.setup()

    try:
        while command != ui.Commands.Quit:
            print('. ')
            time.sleep(0.1)
            command = app_ui.get_command()
            button = app_ui.get_button()

            if button != None:
                if button == Button.BUTTON_1:
                    print('BUTTON_1')
                    app_display.clear_display()
                elif button == Button.BUTTON_2:
                    print('BUTTON_2')
                    app_display.update_display(None)
                elif button == Button.BUTTON_3:
                    print('BUTTON_3')

        kb = KBHit()
        kb.flush()

    except KeyboardInterrupt:
        print('Exiting ...')

    except ZeroOneException as ex:
        print("\n>>> EXCEPTION : {} <<<\n".format(ex.message))
        logging.error(ex.message, exc_info=True)
        app_ui.display_exception(ex.error_code)

    finally:
        app_display.shutdown()

        logging.info('Done!')
        destroy_logging()
        print('Done!')

if __name__ == '__main__':
    main(sys.argv[1:])