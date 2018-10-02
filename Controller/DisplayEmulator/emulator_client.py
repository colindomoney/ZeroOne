import ZO
import logging, sys
from pynput.keyboard import Key, Listener

# Create a class to process key presses
class KeyboardDriver():
    def __init__(self):
        print('KeyboardDriver::__init__()')

        # Setup the hook functions
        self.listener = Listener(
            on_press=self.__on_press__,
            on_release=self.__on_release__)

    def __on_press__(self, key):
        try:
            ch = key.char

            if not self.Keys.contains(ch):
                self.__client_on_press(key)
            else:
                if self.keyEvents[ch] != ButtonEvent.BUTTON_DOWN:
                    self.keyEvents[ch] = ButtonEvent.BUTTON_DOWN
                    if self.keyHandler[ch] != None:
                        self.keyHandler[ch](self.Keys.byvalue(ch), ButtonEvent.BUTTON_DOWN)

            # print('Key = {0}'.format(ch))
        except AttributeError:
            self.__client_on_press(key)

    def __on_release__(self, key):
        try:
            ch = key.char

            if not self.Keys.contains(ch):
                self.__client_on_release(key)
            else:
                if self.keyEvents[ch] != ButtonEvent.BUTTON_UP:
                    self.keyEvents[ch] = ButtonEvent.BUTTON_UP
                    if self.keyHandler[ch] != None:
                        self.keyHandler[ch](self.Keys.byvalue(ch), ButtonEvent.BUTTON_UP)

        except AttributeError:
            self.__client_on_release(key)

print('Done!')

if __name__ == '__main__':
    def setup_logging():
        print("setup_logging")

        logging.basicConfig(
            format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
            handlers=[
                logging.FileHandler("./emulator_client.log"),
                logging.StreamHandler(sys.stdout)
            ])

        global log
        log = logging.getLogger('zero_one')
        log.setLevel(logging.INFO)

    def destroy_logging():
        print("destroy_logging")

    # Start the main program here

    print('emulator_client running ...')
    setup_logging()

    try:
        keyboard = KeyboardDriver()

        while True:
            pass

    except KeyboardInterrupt as ex:
        print('Forcing a quit')
        pass

    except Exception as ex:
        print("\n>>> EXCEPTION : {} <<<\n".format(ex.message))
        log.error(ex.message, exc_info=True)
        pass

    destroy_logging()
    print('Done!')

