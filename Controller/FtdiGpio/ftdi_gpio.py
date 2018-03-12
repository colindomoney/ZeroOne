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

        devices = self._get_ftdi_device_list()
        print(devices)

        self._bb = ftdi.BitBangDevice(device_id='A50285BI', direction=ftdi.ALL_OUTPUTS)

        self._bb.port = 0xff;
        self._bb.port = 0x00;


        print(self._bb)

        # Did we get a device here yet ? If not abort since we can't do anything more

        # Open the device

    # Do the context manager stuff
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO : Close the FTDI device
        pass

    def _get_ftdi_device_list(self):
        """
        return a list of lines, each a colon-separated
        vendor:product:serial summary of detected devices
        """
        dev_list = []
        for device in ftdi.Driver().list_devices():
            # list_devices returns bytes rather than strings
            dev_info = map(lambda x: x.decode('latin1'), device)
            # device must always be this triple
            vendor, product, serial = dev_info
            # dev_list.append("%s:%s:%s" % (vendor, product, serial))
            dev_list.append((vendor, product, serial))
        return dev_list

    # TODO : Set the port directions
    def set_direction(self, map=0):
        pass

    # TODO : Test the bit
    def test_bit(self, bit=0):
        pass

    # TODO : Set the bit high
    def set_bit_high(self, bit=0):
        pass

    # TODO : Set the bit low
    def set_bit_low(self, bit=0):
        pass
