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

    PIN_ALL = 0xff
    PIN0_PIN = 0x01
    PIN1_PIN = 0x02
    PIN2_PIN = 0x04
    PIN3_PIN = 0x08
    PIN4_PIN = 0x10
    PIN5_PIN = 0x20
    PIN6_PIN = 0x40
    PIN7_PIN = 0x80

    PIN_ALL_OUT = 0xff
    PIN0_OUT = 0x01
    PIN1_OUT = 0x02
    PIN2_OUT = 0x04
    PIN3_OUT = 0x08
    PIN4_OUT = 0x10
    PIN5_OUT = 0x20
    PIN6_OUT = 0x40
    PIN7_OUT = 0x80

    PIN_ALL_IN = 0x00
    PIN0_IN = 0x00
    PIN1_IN = 0x00
    PIN2_IN = 0x00
    PIN3_IN = 0x00
    PIN4_IN = 0x00
    PIN5_IN = 0x00
    PIN6_IN = 0x00
    PIN7_IN = 0x00

    def __init__(self, device_id=None):
        self._device_id = device_id

        if self._device_id is None:
            # Search all the availabe devices and pick the first one
            self._device_id = (self._get_ftdi_device_list() or [None])[0]

        print('Device: {}'.format(self._device_id))

        # self._bb = ftdi.BitBangDevice(device_id='A50285BI', direction=ftdi.ALL_OUTPUTS)
        #
        # self._bb.port = 0xff;
        # self._bb.port = 0x00;
        #
        # print(self._bb)

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

            # We used to return a whole ton of stuff
            # dev_list.append("%s:%s:%s" % (vendor, product, serial))

            # Now just return the serial number
            dev_list.append(serial)
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
