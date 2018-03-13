"""
    A helper file to do useful things with images
"""

import numpy, os
from . import zero_one
from PIL import Image

# TODO : How safe is this in practice
ZERO_ONE_MASK_FILE = './ZO/zero_one.npy'

class ZO_Mask:
    '''
    A simple class to manage the '01' pixel mask.
    '''
    def __init__(self):
        self._load_mask_data()

    def _load_mask_data(self):
        ''' Loads the pixel data from the file '''
        self._data = list(numpy.load(ZERO_ONE_MASK_FILE).flatten())

        if len(self._data) != zero_one.ZO_X_SIZE * zero_one.ZO_Y_SIZE:
            raise zero_one.ZeroOneException('Mask data not the correct size')

    #  Returns it as a flattened list
    @property
    def flat(self):
        return list(numpy.load(ZERO_ONE_MASK_FILE).flatten())

    # Returns it as a 2D array
    @property
    def array(self):
        return list(numpy.load(ZERO_ONE_MASK_FILE))

class ZO_Image(Image.Image):
    class Patterns:
        ZeroOutline = 0x01,
        ZeroInterior = 0x02,
        ZeroBoth = 0x03,
        OneOutline = 0x10,
        OneInterior = 0x20,
        OneBoth = 0x30

    def __init__(self):
        super().__init__()

        self._image = None

    @property
    def screen_buffer(self):
        return None

    def set_to_color(self, rgb='black', alpha=0.0):
        pass

    def load_from_file(self, filename=None):
        pass

    def set_pattern(self, pattern=None, rgb='white', alpha=0.0):
        pass

class PixelDriver:
    def __init__(self):
        pass

    def update_display(self):
        ''' Actually write the pixels to the display'''
        pass

    # TODO :