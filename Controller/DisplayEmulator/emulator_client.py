import ZO
import logging, sys, time, fnmatch, os
import kbhit as KBHit
from enum import Enum
from PIL import ImageTk, Image
import pickle
import pprint
from pynput.keyboard import Key, Listener

IMAGE_PATH = '/Users/colind/Documents/Projects/ZeroOne/ZeroOne/Graphics/Images'

def get_images():
    return fnmatch.filter(os.listdir(IMAGE_PATH), '*.png')

# Create a class to process key presses
class KeyboardDriver():
    class Commands(Enum):
        Quit = 100
        Command1 = 1
        Command2 = 2
        Command3 = 3
        Command4 = 4
        Command5 = 5
        Command6 = 6
        Command7 = 7
        Command8 = 8
        Command9 = 9
        Command10 = 0
        Test = 101

        @classmethod
        def contains(cls, key):
            return any(key == item.value for item in cls)

        @classmethod
        def byvalue(cls, val):
            for item in cls:
                if item.value == val:
                    return item
            return None

    def __init__(self):
        print('KeyboardDriver::__init__()')

        self._command = None

        # Setup the hook functions
        self.listener = Listener(
            on_press=self.__on_press__,
            on_release=self.__on_release__)

        self.listener.start()
        self.listener.wait()

    def get_command(self):
        rVal = self._command
        self._command = None
        return rVal

    def __on_press__(self, key):
        # For this case we can simply ignore the key down event
        try:
            ch = ord(key.char) - ord('0')

            if self.Commands.contains(ch):
                self._command = self.Commands.byvalue(ch)

        except AttributeError:
            pass

    def __on_release__(self, key):
        try:
            ch = key.char
            # print('U = {0}'.format(ch))

        except AttributeError:
            if key == Key.esc:
                self._command = self.Commands.Quit

class EmulatorCommand():
    def __init__(self, command = 'None', data=None):
        self.Command = command
        self.Data = data

def send_file(fileNumber):
    files = get_images()

    if fileNumber < len(files):
        pilImg = Image.open(os.path.join(IMAGE_PATH, files[fileNumber]))
        rawData = pilImg.tobytes()

        ec = EmulatorCommand(data=rawData)
        data_string = pickle.dumps(ec)
        newEc = pickle.loads(data_string)

        print(newEc.Command)

    else:
        raise ValueError('Too much files')

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

    send_file(1)
    quit(0)

    try:
        keyboard = KeyboardDriver()
        command = None

        # Loop forever
        while command != keyboard.Commands.Quit:
            command = keyboard.get_command()
            print('. ')
            time.sleep(0.2)

            # Process the command
            if command == keyboard.Commands.Command1:
                print('Command1')
                send_file(1)
            elif command == keyboard.Commands.Command2:
                print('Command2')
                send_file(2)

    # This is kinda normal - just exit
    except KeyboardInterrupt as ex:
        print('Forcing a quit')
        pass

    # We got something we really weren't expecting here
    except Exception as ex:
        print("\n>>> EXCEPTION : {} <<<\n".format(ex.message))
        log.error(ex.message, exc_info=True)
        pass

    # Flush the keyboard here
    kb = KBHit.KBHit()
    kb.flush()

    # Shut this puppy down
    destroy_logging()
    print('Done!')

