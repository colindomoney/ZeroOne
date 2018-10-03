import ZO
import logging, sys, time, fnmatch, os, socket
import kbhit as KBHit
from enum import Enum
from PIL import ImageTk, Image
import pickle, random, timer_cm
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
        # print('KeyboardDriver::__init__()')

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


# TODO : God this has to be duplicated on both the client and server
class EmulatorCommand():
    def __init__(self, command = 'None', data=None):
        self.command = command
        self.data = data


# TODO : This is going to end up deriving from an interface shared by the 01 sometime
class ZeroOneEmulator():
    # Define some strings for the commands we'll use
    Commands = ['DisplayAll', 'DisplayZeroOne', 'ClearDisplay']

    def __init__(self):
        # print('ZeroOneEmulator::__init__()')

        self._port = 6999
        self._host = socket.gethostname()
        self._client = None
        self._connected = False  # Shows if we are connected or not

    @property
    def connected(self):
        return self._connected

    # Do the useful commands here
    def display_full_image(self, raw_data=None, filename=None):
        print('display_full_image')

    def display_full_image(self, raw_data=None, filename=None):
        print('display_full_image', filename)

        pil_img = Image.open(filename)
        width, height = pil_img.size

        if width != ZO.ZO_X_SIZE and height != ZO.ZO_Y_SIZE:
            raise ZO.ZeroOneException('File not a ZeroOne file')

        # TODO: Make sure everything else works with RGB only
        pil_img = pil_img.convert('RGB')

        self._do_command(EmulatorCommand('DisplayAll', pil_img.tobytes()))

        # new_pil_img = Image.frombytes('RGB', (ZO.zero_one.ZO_X_SIZE, ZO.zero_one.ZO_Y_SIZE), pil_img.tobytes(), 'raw')
        # new_pil_img.show()

    def clear_display(self):
        print('clear_display')
        self._do_command(EmulatorCommand('ClearDisplay'))

    def _do_command(self, ec):
        data_string = pickle.dumps(ec)

        if self.connected == True:
            # print('len = ', len(data_string))
            # print(data_string)
            self._client.send(data_string)

            # print(data_string)
            emulator_command = pickle.loads(data_string)
            print(emulator_command.command)
        else:
            print('>> Not connected')

    # Arguably not the best place for this but needs must
    def get_random_file(self):
        files = get_images()

        while True:
            max_num = len(files)
            file_number = random.randint(0, max_num - 1)

            file_name = os.path.join(IMAGE_PATH, files[file_number])
            pil_img = Image.open(file_name)
            width, height = pil_img.size

            if width != ZO.ZO_X_SIZE and height != ZO.ZO_Y_SIZE:
                print('File not a ZeroOne file')
                continue
            else:
                return file_name

    # A debug method to be removed
    def debug(self, opt=0):
        print('debug()')

        file_name = self.get_random_file()
        print(file_name)

        zo_image = ZO.ZO_Image()
        zo_image.load_from_file(file_name)

        zo_data = zo_image.zero_one_raw_data

        with timer_cm.Timer('get_image_from_zero_one_data'):
            zo_image.get_image_from_zero_one_data()

        # zo_image.set_pattern(ZO.ZO_Image.Patterns.BothBoth)
        # zo_image.show()

    def send_file(self, file_name=None, file_number=-1, displayMode ='DisplayZeroOne'):
        files = get_images()

        while True:
            if file_number < 0:
                maxNum = len(files)
                file_number = random.randint(0, maxNum - 1)

            if file_number < len(files):
                file_name = os.path.join(IMAGE_PATH, files[file_number])
                pilImg = Image.open(file_name)
                width, height = pilImg.size

                if width != ZO.ZO_X_SIZE and height != ZO.ZO_Y_SIZE:
                    print('File not a ZeroOne file')
                    file_number = -1
                    continue
                else:
                    break
            else:
                raise ValueError('Too much files')

        raw_data = pilImg.tobytes()

        emulator_command = EmulatorCommand(data=raw_data)
        data_string = pickle.dumps(emulator_command)
        new_emulator_command = pickle.loads(data_string)

        print(new_emulator_command.command)

        if self.connected == True:
            print('len = ', len(data_string))
            self._client.send(data_string)

        return 0


    def connect(self):
        self._connected = False
        self._client = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._client.connect((self._host, self._port))
            self._connected = True
            return self._connected

        except Exception as ex:
            print('>> ', ex)
            return self._connected

    def close(self):
        print('close()')
        if self.connected == True:
            self._client.close()


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

        # TODO : This is IDE debugging only, can be remove
        connected = emulator.connect()
        print('Connected = ', emulator.connected)

        # emulator.debug(1)
        emulator.display_full_image(filename=emulator.get_random_file())
        # emulator.clear_display()

        # connected = False

        if connected:
            # Loop forever
            while command != keyboard.Commands.Quit:
                command = keyboard.get_command()
                print('. ')
                time.sleep(0.2)

                # Process the command
                if command == keyboard.Commands.Command1:
                    print('Command1')
                    emulator.debug(1)
                elif command == keyboard.Commands.Command2:
                    print('Command2')
                    emulator.clear_display()
        else:
            print('>> Failed to connect to server, exiting ...')

    # This is kinda normal - just exit
    except KeyboardInterrupt as ex:
        print('Forcing a quit')
        pass

    # We got something we really weren't expecting here
    except Exception as ex:
        print("\n>>> EXCEPTION : {} <<<\n".format(ex))
        log.error(ex, exc_info=True)
        pass

    finally:
        emulator.close()

        # Flush the keyboard here
        try:
            kb = KBHit.KBHit()
            kb.flush()
        except:
            pass

        # Shut this puppy down
        destroy_logging()
        print('Done!')

