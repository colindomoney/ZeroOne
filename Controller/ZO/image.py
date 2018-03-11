"""
    A helper file to do useful things with images
"""

import numpy, os
from . import zero_one

# TODO : How safe is this in practice
ZERO_ONE_MASK_FILE = './ZO/zero_one.npy'

def load_mask_data():

    thisDir = os.getcwd()

    # Get the mask data, flatten it out and convert it to a list
    maskData = list(numpy.load(ZERO_ONE_MASK_FILE).flatten())

    if len(maskData) != zero_one.ZO_X_SIZE * zero_one.ZO_Y_SIZE:
        raise zero_one.ZeroOneException('Mask data not the correct size')

    return maskData