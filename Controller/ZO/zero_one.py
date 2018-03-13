

ZO_PIXEL_COUNT = 591  # The total pixels (ie. LEDs) on the display
ZO_X_SIZE = 38  # The X dimension ie. columns
ZO_Y_SIZE = 28  # The Y dimension ie. rows

# GPIO pinouts
# GPIO2 = pushbutton
# GPIO4 = pushbutton
# GPIO5 = pushbutton
# GPIO17 = LED
# GPIO27 = LED

# TODO : Pull in the '01' pixels and store them as a 591 byte list

# TODO : Definitions for the values in the '01' pixel ie. 11, 22, 1, 2, 0

# TODO : Convery a PNG to a 28x38 thumbnail

class ZeroOneException(Exception):
    """  Massively complex override of the base exception class for ZeroOne exceptions """
    def __init__(self, message):
        super().__init__(self)
        self.message = message

    # Forget to do this and it will recurse like a motherf...er
    def __str__(self):
        return self.message


# TODO : Not sure we need this class any more
class ZeroOne(object):
    def __init__(self):
        pass


class PixelDriver:
    def __init__(self):
        # TODO : Check the display is present ie. server reachable, etc
        pass

    def update_display(self):
        ''' Actually write the pixels to the display'''
        pass

    def _map_image_to_pixels(self):
        from . import ZO_Mask

        maskData = ZO_Mask().flat

        # Zip the data
        # TODO : Set the input data here
        combinedData = list(zip(imgData, maskData))

        # Get everything that isn't a zero in the mask
        outputFrame = [x[0] for x in combinedData if x[1] != 0]

        if len(outputFrame) != ZO_PIXEL_COUNT:
            raise ZeroOneException('Pixel count not the expected length after masking')

    # TODO : Implement the following features
    #  1 - check the server is running
    #  2 - check the displays are attached
    #  3 - blank the pixels

