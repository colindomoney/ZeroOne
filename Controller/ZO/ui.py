import io
from collections import namedtuple
from enum import Enum


def __is_raspberry_pi__(raise_on_errors=False):
    """
    Checks if the platform is a Raspberry Pi by check the 'cpuinfo' file
    :param raise_on_errors: Set to true to throw an exception if it's not a Pi
    :return: True if it's a Pi, false otherwise
    """
    try:
        with io.open('/proc/cpuinfo', 'r') as cpuinfo:
            found = False
            for line in cpuinfo:
                if line.startswith('Hardware'):
                    found = True
                    label, value = line.strip().split(':', 1)
                    value = value.strip()

                    if value not in (
                            'BCM2708',
                            'BCM2709',
                            'BCM2835',
                            'BCM2836'
                    ):
                        if raise_on_errors:
                            raise ValueError(
                                'This system does not appear to be a '
                                'Raspberry Pi.'
                            )
                        else:
                            return False
            if not found:
                if raise_on_errors:
                    raise ValueError(
                        'Unable to determine if this system is a Raspberry Pi.'
                    )
                else:
                    return False
    except IOError:
        if raise_on_errors:
            raise ValueError('Unable to open `/proc/cpuinfo`.')
        else:
            return False

    return True


class Commands(Enum):
    Quit = 0
    Command1 = 1
    Command2 = 2
    Command3 = 3
    Command4 = 4
    Command5 = 5
    Command6 = 6
    Command7 = 7
    Command8 = 8
    Command9 = 9
    Command10 = 10
    Test = 100


class ButtonEvent(Enum):
    BUTTON_DOWN = 1
    BUTTON_UP = 2


class Button(Enum):
    BUTTON_1 = 1
    BUTTON_2 = 2
    BUTTON_3 = 3


class Led(Enum):
    LED_RED = 1
    LED_GREEN = 2


__ui_instance__ = None


class UIBase:
    class LED_State(Enum):
        LED_OFF = 1,
        LED_ON = 2,
        LED_FLASH = 3

    def __str__(self):
        return "UIBase -> Red: {0}, Green: {1}".format(self._leds[Led.LED_RED], self._leds[Led.LED_GREEN])

    def __init__(self):
        self._command = None
        # ledValues = namedtuple('LED_Values', 'state period')

        self._leds = {
            Led.LED_RED : namedtuple('LED_Values', 'state period'),
            Led.LED_GREEN : namedtuple('LED_Values', 'state period')
        }

        self._leds[Led.LED_GREEN].state = UIBase.LED_State.LED_OFF
        self._leds[Led.LED_GREEN].period = 200

        self._leds[Led.LED_RED].state = UIBase.LED_State.LED_OFF
        self._leds[Led.LED_RED].period = 200

    @staticmethod
    def button_handler1(key, button_event):
        print('button_handler1() -> {}, {}'.format(key.value, button_event))

    @staticmethod
    def button_handler2(key, button_event):
        print('button_handler2() -> {}, {}'.format(key.value, button_event))

    @staticmethod
    def button_handler3(key, button_event):
        print('button_handler3() -> {}, {}'.format(key.value, button_event))

    def process_keystroke(self, key):
        print('< {} >'.format(key))

        if key == 0x1c:
            self._command = Commands.Quit
        elif key == 0x20:
            self._command = Commands.Test


    def test_button(self, button=Button.BUTTON_1):
        pass

    def register_button_event_handler(self, callback, button=Button.BUTTON_1):
        pass

    def get_command(self):
        command = self._command
        self._command = None
        return command

    def test(self):
        pass

    def led_flash(self, led, period=500):

        if period < 10:
            period = 10

        self._leds[led].state = UIBase.LED_State.LED_FLASH
        self._leds[led].period = period

    def led_on(self, self1, led):
        self._leds[led].state = UIBase.LED_State.LED_ON

    def led_off(self, self1, led):
        self._leds[led].state = UIBase.LED_State.LED_OFF


def get_ui_instance():
    global __ui_instance__
    if __is_raspberry_pi__():
        import ZO.pi_ui

    else:
        import ZO.pc_ui
        if __ui_instance__ is None:
            __ui_instance__ = ZO.pc_ui.PC_UI()

    return __ui_instance__
