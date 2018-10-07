import time

import psutil, sys, os, signal
import opc
from PIL import Image
from ZO import *

# This file is responsible for driving the displays on the ZeroOne

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Display(metaclass=Singleton):
# class Display():
    def __init__(self, fadecandy_config, ):
        print('Display::__init__()')

        this_directory = os.path.dirname(os.path.realpath(__file__))
        if this_directory.endswith('/ZO'):
            this_directory = this_directory[:-3]

        self._fcserver = None

        if fadecandy_config['Enabled'] != 0:
            self._fcserver = FCServer(os.path.join(this_directory, fadecandy_config['BinaryPath']),
                                      os.path.join(this_directory, fadecandy_config['ConfigPath']))

            print(self._fcserver)

    def __str__(self):
        return "Display() -> {0}".format(self.__hash__())

    def test(self):
        pass

    # Setup the display servers
    def setup(self):
        if self._fcserver != None:
            self._fcserver.setup()

    # Shutdown the display servers
    def shutdown(self):
        if self._fcserver != None:
            self._fcserver.shutdown()

    # The actual methods to write to the display
    def clear_display(self):
        if self._fcserver != None:
            self._fcserver.clear_display()

    def update_display(self, img):
        if self._fcserver != None:
            test_img = ZO_Image()
            test_img.load_from_file(TEST_PATTERN_FILE)

            self._fcserver.update_display(test_img.image)

class FCServer():
    # Construct with the path to the binary and its config file
    def __init__(self, binary_path=None, config_path=None):
        self._binary_path = binary_path
        self._config_path = config_path
        self._process = None
        self._pixel_driver = None

        if os.path.exists(binary_path) == False:
            raise ZeroOneException("fcserver binary does not exist -> {0}".format(binary_path))

        if os.path.exists(config_path) == False:
            raise ZeroOneException("fcserver config file does not exist -> {0}".format(config_path))

    def __str__(self):
        return "FCServer() -> Exe: {0}, Config: {1}".format(self._binary_path, self._config_path)

    def shutdown(self):
        self._kill_existing_instances()

    def setup(self):
        self._kill_existing_instances()
        return self._run_server()

    def test(self):
        pass

    def _find_procs_by_name(self, name):
        ls = []
        for p in psutil.process_iter(attrs=['name']):
            if name in p.info['name']:
                ls.append(p)
        return ls

    # Finds and kills any existing instances of the server
    def _kill_existing_instances(self):
        if self._process != None:
            self._process.send_signal(signal.SIGTERM)
        else:
            pids = self._find_procs_by_name('fcserver')
            print(pids)

            # Loop ... a bit
            for i in range(10):
                for pid in pids:
                    print('isrunning', pid.is_running())
                    print('status()', pid.status())
                    pid.send_signal(signal.SIGTERM)

                if len(self._find_procs_by_name('fcserver')) == 0:
                    break

                # print('sleep ...')
                time.sleep(0.25)

    # Runs the server as a new process and returns straight away
    def _run_server(self):
        self._process = psutil.Popen([self._binary_path, self._config_path])
        time.sleep(0.2)
        self._pixel_driver = PixelDriver()
        return True if self._pixel_driver.can_connect() else False

    # Does a simple loopback test to see if the server is running
    # def _verify_server(self):
    #     self._pixel_driver = PixelDriver()
    #     return True if self._pixel_driver.can_connect() else False

    def clear_display(self):
        self._pixel_driver.clear_display()

    def update_display(self, img):
        self._pixel_driver.update_display(img)

# This is the OPC driver class
class PixelDriver:
    OpcConnectionString = 'localhost:7890'

    def __init__(self):
        self._interpolation = False
        self._client = opc.Client(PixelDriver.OpcConnectionString)
        self._client.set_interpolation(self._interpolation)

    def can_connect(self):
        return self._client.can_connect()

    def connect_to_server(self):
        if not self._client.can_connect():
            raise ZeroOneException('Failed to connect to OPC server at {0}'.format(PixelDriver.OpcConnectionString))

    def update_display(self, image=None):
        print('update_display()')

        ''' Actually write the pixels to the display'''
        self.connect_to_server()

        if image is not None:
            self._map_image_to_pixels(image)

    @property
    def interpolation(self):
        return self._interpolation

    @interpolation.setter
    def interpolation(self, value):
        self.interpolation = value
        self._client.set_interpolation(self._interpolation)

    def clear_display(self):
        print('clear_display()')
        black = [(0, 0, 0)] * ZO_X_SIZE * ZO_Y_SIZE
        self._client.set_interpolation(False)
        self._client.put_pixels(black)
        self._client.set_interpolation(self._interpolation)

    def _map_image_to_pixels(self, opImage):
        from . import ZO_Mask

        maskData = ZO_Mask().flat

        # Zip the data
        combinedData = list(zip(list(opImage.getdata()), maskData))

        # Get everything that isn't a zero in the mask
        outputFrame = [x[0] for x in combinedData if x[1] != 0]

        if len(outputFrame) != ZO_PIXEL_COUNT:
            raise ZeroOneException('Pixel count not the expected length after masking')

        # TODO : This can throw an exception if the input format ia wrong
        pixels = [(x[0], x[1], x[2]) for x in outputFrame]

        self._client.put_pixels(pixels)

