"""
    A helper file to do useful things with images
"""

import numpy, os
from . import zero_one
from PIL import Image, ImageColor

# TODO : How safe is this in practice
ZERO_ONE_MASK_FILE = './ZO/zero_one.npy'

TEST_PATTERN_FILE = '/Users/colind/Projects/ZeroOne/ZeroOne/Graphics/Images/RGBW.png'
RED_TEST_PATTERN_FILE = '/Users/colind/Projects/ZeroOne/ZeroOne/Graphics/Images/Red_Left.png'
GREEN_TEST_PATTERN_FILE = '/Users/colind/Projects/ZeroOne/ZeroOne/Graphics/Images/Green_Centre.png'
BLUE_TEST_PATTERN_FILE = '/Users/colind/Projects/ZeroOne/ZeroOne/Graphics/Images/Blue_Right.png'

class ZO_Mask:
    # This tag values in the CSV pattern file
    class ZoneTags:
        NoTag = 0
        ZeroOutlineTag = 11
        ZeroInteriorTag = 1
        OneOutlineTag = 22
        OneInteriorTag = 2

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
        return numpy.load(ZERO_ONE_MASK_FILE).tolist()

class ZO_Image:
    class Patterns:
        ZeroOutline = 0x01
        ZeroInterior = 0x02
        ZeroBoth = 0x03
        OneOutline = 0x10
        OneInterior = 0x20
        OneBoth = 0x30

    def __init__(self):
        super().__init__()

        self._image = None
        self._pattern = None

    # TODO : Return the underlying image buffer
    @property
    def screen_buffer(self):
        return None

    # TODO : Not sure what this was going to do ?
    # def set_to_color(self, rgb='black', alpha=0.0):
    #     pass

    def load_from_file(self, filename=None):
        self._image = Image.open(filename)
        # self._image.show()

    def clear_pattern(self):
        # Create a new image in RGBA with (width, height)
        self._pattern = Image.new('RGBA', (zero_one.ZO_X_SIZE, zero_one.ZO_Y_SIZE))

    def set_pattern(self, pattern=None, rgb='red', alpha=255, show=False):
        mask = ZO_Mask().array

        if self._pattern is None:
            self.clear_pattern()

        bg = ImageColor.getcolor('white', 'RGBA')
        bg = (bg[0], bg[1], bg[2], 0)  # Set a transparent background
        fg = ImageColor.getcolor(rgb, 'RGBA')
        fg = (fg[0], fg[1], fg[2], alpha)  # Set a transparent background

        op = []
        for r in mask:
            row = []
            for c in r:
                if c == ZO_Mask.ZoneTags.NoTag:
                    row.append(bg)
                elif c == ZO_Mask.ZoneTags.OneInteriorTag:
                    row.append(fg if pattern & ZO_Image.Patterns.OneInterior else bg)
                elif c == ZO_Mask.ZoneTags.OneOutlineTag:
                    row.append(fg if pattern & ZO_Image.Patterns.OneOutline else bg)
                elif c == ZO_Mask.ZoneTags.ZeroOutlineTag:
                    row.append(fg if pattern & ZO_Image.Patterns.ZeroOutline else bg)
                elif c == ZO_Mask.ZoneTags.ZeroInteriorTag:
                    row.append(fg if pattern & ZO_Image.Patterns.ZeroInterior else bg)

            op.append(row)

        # Some clever fannying around to make sure we keep the tuple data correctly
        op = numpy.asarray(op, dtype=numpy.dtype('uint8,uint8,uint8,uint8'))
        wcImg = Image.fromarray(op, 'RGBA')

        # Now paste the temporary image over the pattern
        self._pattern =  Image.alpha_composite(self._pattern, wcImg)

        if show == True:
            self._pattern.show()