import ZO
import logging, sys, time, fnmatch, os, socket
import kbhit as KBHit
from enum import Enum
from PIL import ImageTk, Image
import pickle, random
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

# TODO : This is going to end up deriving from an interface shared by the 01 sometime
class ZeroOneEmulator():
    def __init__(self):
        print('ZeroOneEmulator::__init__()')

        self._port = 6999
        self._host = socket.gethostname()
        self._client = None
        self._connected = False  # Shows if we are connected or not

    @property
    def connected(self):
        return self._connected

    def send_file(self, fileName=None, fileNumber=0, displayMode = 'DisplayZeroOne'):
        files = get_images()

        if fileNumber < len(files):
            pilImg = Image.open(os.path.join(IMAGE_PATH, files[fileNumber]))
            rawData = pilImg.tobytes()

            ec = EmulatorCommand(data=rawData)
            data_string = pickle.dumps(ec)
            newEc = pickle.loads(data_string)

            print(newEc.Command)

            if self.connected == True:
                print('len = ', len(data_string))
                self._client.send(data_string)

        else:
            raise ValueError('Too much files')

    def connect(self):
        self._connected = False
        self._client = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM)

        # self._client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        try:
            self._client.connect((self._host, self._port))
            self._connected = True
            return self._connected

        except Exception as ex:
            print('>> ', ex)
            return self._connected

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
        command = None

        emulator = ZeroOneEmulator()
        connected = emulator.connect()
        print('Connected = ', emulator.connected)

        if connected == True:
            files = get_images()
            maxNum = len(files)

            # Loop forever
            while command != keyboard.Commands.Quit:
                command = keyboard.get_command()
                print('. ')
                time.sleep(0.2)

                thisFile = random.randint(0, maxNum-1)

                # Process the command
                if command == keyboard.Commands.Command1:
                    print('Command1', thisFile)
                    emulator.send_file(fileNumber=thisFile)
                elif command == keyboard.Commands.Command2:
                    print('Command2', thisFile)
                    emulator.send_file(fileNumber=thisFile)
        else:
            print('>> Failed to connect to server, exiting ...')

    # This is kinda normal - just exit
    except KeyboardInterrupt as ex:
        print('Forcing a quit')
        pass

    # We got something we really weren't expecting here
    except Exception as ex:
        print("\n>>> EXCEPTION : {} <<<\n".format(ex.message))
        log.error(ex.message, exc_info=True)
        pass

    finally:
        # Flush the keyboard here
        try:
            kb = KBHit.KBHit()
            kb.flush()
        except:
            pass

        # Shut this puppy down
        destroy_logging()
        print('Done!')

