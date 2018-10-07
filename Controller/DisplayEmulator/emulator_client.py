from ZO import EmulatorCommand, ZO_Image, ZO_Y_SIZE, ZO_X_SIZE, ZeroOneException
import logging, sys, time, fnmatch, os, socket
import kbhit as KBHit
from enum import Enum
from PIL import Image
import random, timer_cm, pprint, dill
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
    def display_zero_one_image(self, raw_data=None, filename=None):
        print('display_zero_one_image', filename)

        pil_img = Image.open(filename)
        width, height = pil_img.size

        if width !=  ZO_X_SIZE and height != ZO_Y_SIZE:
            raise ZeroOneException('File not a ZeroOne file')

        # Now convert to 01 format
        zo_image = ZO_Image()
        zo_image.load_from_file(filename)

        self._do_command(EmulatorCommand.EmulatorCommand('DisplayZeroOne', zo_image.zero_one_raw_data))

    def display_full_image(self, image=None, filename=None):
        print('display_full_image', filename)

        if filename != None:
            pil_img = Image.open(filename)
        elif image != None:
            pil_img = image

        width, height = pil_img.size

        if width != ZO_X_SIZE and height != ZO_Y_SIZE:
            raise ZeroOneException('File not a ZeroOne file')

        pil_img = pil_img.convert('RGB')

        self._do_command(EmulatorCommand.EmulatorCommand('DisplayAll', pil_img.tobytes()))

    def clear_display(self):
        print('clear_display')
        self._do_command(EmulatorCommand.EmulatorCommand('ClearDisplay'))

    def _do_command(self, ec):
        data_string = dill.dumps(ec)

        if self.connected == True:
            self._client.send(data_string)

            emulator_command = dill.loads(data_string)
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

            if width != ZO_X_SIZE and height != ZO_Y_SIZE:
                print('File not a ZeroOne file')
                continue
            else:
                return file_name

    # A debug method to be removed
    def debug(self, opt=0):
        print('debug()')

        file_name = self.get_random_file()
        # print(file_name)

        zo_image = ZO_Image()
        zo_image.load_from_file(file_name)

        zo_data = zo_image.zero_one_raw_data

        with timer_cm.Timer('get_image_from_zero_one_data'):
            zo_image.get_image_from_zero_one_data()

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

                if width != ZO_X_SIZE and height != ZO_Y_SIZE:
                    print('File not a ZeroOne file')
                    file_number = -1
                    continue
                else:
                    break
            else:
                raise ValueError('Too much files')

        raw_data = pilImg.tobytes()

        emulator_command = EmulatorCommand.EmulatorCommand(data=raw_data)
        data_string = dill.dumps(emulator_command)
        new_emulator_command = dill.loads(data_string)

        print(new_emulator_command.command)

        if self.connected == True:
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
        print('ZeroOneEmulator::close()')
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
        log = logging.getLogger('emulator_client')
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

        # TODO : This is IDE debugging only, can be removed
        connected = emulator.connect()
        print('Connected = ', emulator.connected)
        emulator.clear_display()

        if connected:
            # Loop forever
            while command != keyboard.Commands.Quit:
                command = keyboard.get_command()
                print('. ')
                time.sleep(0.1)

                # Process the command
                if command == keyboard.Commands.Command1:
                    print('Command1')
                    # emulator.display_full_image(filename=emulator.get_random_file())
                    emulator.display_full_image(filename='/Users/colind/Documents/Projects/ZeroOne/ZeroOne/Graphics/Images/RGBW.png')
                elif command == keyboard.Commands.Command2:
                    print('Command2')
                    emulator.display_zero_one_image(filename=emulator.get_random_file())
                elif command == keyboard.Commands.Command3:
                    print('Command3')
                    emulator.clear_display()
        else:
            print('Failed to connect to server, exiting ...')

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

