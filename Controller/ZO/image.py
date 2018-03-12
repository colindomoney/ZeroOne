"""
    A helper file to do useful things with images
"""

import numpy, os
from . import zero_one

# TODO : How safe is this in practice
ZERO_ONE_MASK_FILE = './ZO/zero_one.npy'

# TODO : Put this in a nice class and enable it to return a flat list of a shape
def load_mask_data():

    # Get the mask data, flatten it out and convert it to a list
    maskData = list(numpy.load(ZERO_ONE_MASK_FILE).flatten())

    if len(maskData) != zero_one.ZO_X_SIZE * zero_one.ZO_Y_SIZE:
        raise zero_one.ZeroOneException('Mask data not the correct size')

    return maskData

#  TODO : Extend the PIL:Image class to be able to draw borders and shapes with the '01' mask