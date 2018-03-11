"""
    A helper file to do useful things with images
"""

import numpy
from . import zero_one

ZERO_ONE_MASK_FILE = '/Users/colind/Projects/ZeroOne/ZeroOne/Controller/ZO/zero_one.npy'

def load_mask_data():

    # Get the mask data, flatten it out and convert it to a list
    maskData = list(numpy.load(ZERO_ONE_MASK_FILE).flatten())

    return maskData