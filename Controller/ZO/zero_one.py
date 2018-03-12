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


class ZeroOne(object):

    def __init__(self):
        pass

# TODO : Add a class that controls the pixels ie. checks the server is there, can blit images to the pixels
