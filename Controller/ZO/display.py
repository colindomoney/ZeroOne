import psutil, sys, os, signal
import opc
from PIL import Image
from ZO import *

# This file is responsible for driving the displays on the ZeroOne

class FCServer():
    # Construct with the path to the binary and its config file
    def __init__(self, binary_path=None, config_path=None):
        pass

    def _find_procs_by_name(name):
        ls = []
        for p in psutil.process_iter(attrs=['name']):
            if name in p.info['name']:
                ls.append(p)
        return ls

    # Finds and kills any existing instances of the server
    def _kill_existing_instances(self):
        pids = self._find_procs_by_name('fcserver')
        print(pids)

        if len(pids) != 0:
            pids[0].send_signal(signal.SIGTERM)

        pids = self._find_procs_by_name('fcserver')
        print(pids)

    # Runs the server as a new process and returns straight away
    def _run_server(self):
        pass

    # Does a simple loopback test to see if the server is running
    def _verify_server(self):
        pixel_driver = PixelDriver()
        return True if pixel_driver.can_connect() else False

# This is the OPC driver class
class PixelDriver:
    OpcConnectionString = 'localhost:7890'

    def __init__(self):
        self._interpolation = True
        self._client = opc.Client(PixelDriver.OpcConnectionString)
        self._client.set_interpolation(self._interpolation)

    def can_connect(self):
        return self.can_connect()

    def connect_to_server(self):
        if not self._client.can_connect():
            raise ZeroOneException('Failed to connect to OPC server at {0}'.format(PixelDriver.OpcConnectionString))

    def update_display(self, image=None):
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

    def blank_display(self):
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


# An abstract base class for a display device, either emulator or physical
class DisplayDevice():
    def __init__(self):
        pass