class FtdiGpioException(Exception):
    """  Massively complex override of the base exception class for ZeroOne exceptions """

    def __init__(self, message):
        super().__init__(self)
        self.message = message

    # Forget to do this and it will recurse like a motherf...er
    def __str__(self):
        return self.message


try:
    import pylibftdi as ftdi
except ImportError:
    raise FtdiGpioException(
        'Failed to import the pylibftdi module - install this with Pip and the associated low-level driver')


class FtdiGpio:
    # TODO : Define the pin maps here in hex

    # TODO : Define the I/O direction

    def __init__(self, device_id=None):
        self._device_id = None

        if device_id is None:
            # Search all the availabe devices and pick the first one
            pass

        # Did we get a device here yet ? If not abort since we can't do anything more

        # Open the device

    # Do the context manager stuff
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def set_direction(self, map=0):
        pass

    def test_bit(self, bit=0):
        pass

    def set_bit_high(self, bit=0):
        pass

    def set_bit_low(self, bit=0):
        pass
