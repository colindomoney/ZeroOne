import io
from enum import Enum
import threading

import sys


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


    class LED_Values:
        def __init__(self, state, period=200):
            self.state = state
            self.period = period

        def __str__(self):
            return str("State: {0}, Period: {1}".format(self.state, self.period))

    def __str__(self):
        return "UIBase -> Red: {0}, Green: {1}".format(self._leds[Led.LED_RED], self._leds[Led.LED_GREEN])

    def __init__(self):
        self._command = None

        self._leds = {
            Led.LED_RED: r,
            Led.LED_GREEN: g
        }

        self._leds[Led.LED_GREEN].period = 0.2
        self._leds[Led.LED_GREEN].state = UIBase.LED_State.LED_OFF

        self._leds[Led.LED_RED].period = 0.2
        self._leds[Led.LED_RED].state = UIBase.LED_State.LED_OFF

    @staticmethod
    def button_handler1(key, button_event):
        print('button_handler1() -> {}, {}'.format(key.value, button_event))

    @staticmethod
    def button_handler2(key, button_event):
        print('button_handler2() -> {}, {}'.format(key.value, button_event))

    @staticmethod
    def button_handler3(key, button_event):
        print('button_handler3() -> {}, {}'.format(key.value, button_event))

    def _red_flash(self):
        pass

    def _green_flash(self):
        print('Enter _green_flash()')

        if self._leds[Led.LED_GREEN].period != 0:
            if self._leds[Led.LED_GREEN].state == UIBase.LED_State.LED_OFF:
                self._leds[Led.LED_GREEN].state = UIBase.LED_State.LED_ON
                # self.led_on(Led.LED_GREEN)
            else:
                self._leds[Led.LED_GREEN].state = UIBase.LED_State.LED_OFF
                # self.led_off(Led.LED_GREEN)

            print('.. call')
            try:
                threading.Timer(self._leds[Led.LED_GREEN].period, self._green_flash).start()
            except:
                print(sys.exc_info())
            print('.. done')
        else:
            self.led_off(Led.LED_GREEN)

        print('Exit _green_flash()')

    def _do_flash(self, led):
        print('_do_flash()')

        if self._leds[led].state == UIBase.LED_State.LED_FLASH:
            if self._leds[led].nextState == UIBase.LED_State.LED_ON:
                self._leds[led].nextState = UIBase.LED_State.LED_OFF
                self.led_on(led)
            else:
                self._leds[led].nextState = UIBase.LED_State.LED_ON
                self.led_off(led)

            print('.. call')
            # TODO : Use the 'args' value here
            threading.Timer(self._leds[led].period, self._do_flash, [led]).start()
            print('.. done')
        else:
            self._leds[led].nextState = UIBase.LED_State.LED_ON

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

    def led_flash(self, led, period=0.25):

        if period < 0.005:
            period = 0.005

        self._leds[led].period = period

        if led == Led.LED_GREEN:
            self._green_flash()
        else:
            self._red_flash()

    def led_on(self, led):
        self._leds[led].state = UIBase.LED_State.LED_ON
        self.set_led(led, UIBase.LED_State.LED_ON)

    def led_off(self, led):
        self._leds[led].state = UIBase.LED_State.LED_OFF
        self.set_led(led, UIBase.LED_State.LED_OFF)

    def set_led(self, led, state):
        pass

    def shutdown(self):
        # TODO : Turn the LEDs off and stop flashing
        #  Should just be able to call led_off() here
        self._leds[Led.LED_GREEN].period = 0
        self._leds[Led.LED_GREEN].state = UIBase.LED_State.LED_OFF

        self._leds[Led.LED_RED].period = 0
        self._leds[Led.LED_RED].state = UIBase.LED_State.LED_OFF


def get_ui_instance():
    global __ui_instance__
    if __is_raspberry_pi__():
        import ZO.pi_ui

    else:
        import ZO.pc_ui
        if __ui_instance__ is None:
            __ui_instance__ = ZO.pc_ui.PC_UI()

    return __ui_instance__
