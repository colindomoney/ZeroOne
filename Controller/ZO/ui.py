import io, collections
import time
from enum import Enum
import threading

import sys


def _is_raspberry_pi(raise_on_errors=False):

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
    BUTTON_1 = 1  # Outer Red button
    BUTTON_2 = 2  # Middle Red button
    BUTTON_3 = 3  # Black button


class Led(Enum):
    LED_RED = 1
    LED_GREEN = 2
    LED_AMBER = 3


_ui_instance = None


class UIBase:
    class LED_State(Enum):
        LED_OFF = 1,
        LED_ON = 2,
        LED_FLASH = 3

    class LED_Values:
        def __init__(self, state, period=0.2):
            self.state = state
            self.period = period
            self.nextState = UIBase.LED_State.LED_ON

        def __str__(self):
            return str("State: {0}, Period: {1}".format(self.state, self.period))

    def __str__(self):
        return "UIBase -> Red: {0}, Green: {1}".format(self._leds[Led.LED_RED], self._leds[Led.LED_GREEN])

    def __init__(self):
        self._command = None
        self._running = True

        self._leds = {
            Led.LED_RED: UIBase.LED_Values(UIBase.LED_State.LED_OFF),
            Led.LED_GREEN: UIBase.LED_Values(UIBase.LED_State.LED_OFF),
            Led.LED_AMBER: UIBase.LED_Values(UIBase.LED_State.LED_OFF)
        }

        self._leds[Led.LED_GREEN].period = 0.2
        self._leds[Led.LED_GREEN].state = UIBase.LED_State.LED_OFF

        self._leds[Led.LED_RED].period = 0.2
        self._leds[Led.LED_RED].state = UIBase.LED_State.LED_OFF

        self._leds[Led.LED_AMBER].period = 0.2
        self._leds[Led.LED_AMBER].state = UIBase.LED_State.LED_OFF

        self._queue = collections.deque()

    def _do_flash(self, led):
        if self._leds[led].state == UIBase.LED_State.LED_FLASH:
            if self._leds[led].nextState == UIBase.LED_State.LED_OFF:
                self._leds[led].nextState = UIBase.LED_State.LED_ON
                self._set_led(led, UIBase.LED_State.LED_OFF)
            else:
                self._leds[led].nextState = UIBase.LED_State.LED_OFF
                self._set_led(led, UIBase.LED_State.LED_ON)

            if self._running:
                threading.Timer(self._leds[led].period, self._do_flash, [led]).start()
        else:
            self.led_off(led)

    def process_keystroke(self, key):
        '''

        @param key:
        @type key:
        @return:
        @rtype:
        '''
        # print('< {} >'.format(key))

        if key == 0x1c:
            self._command = Commands.Quit
        elif key == 0x20:
            self._command = Commands.Test

    def test_button(self, button=Button.BUTTON_1):
        pass

    def get_button(self):
        if len(self._queue) != 0:
            return self._queue.pop()
        else:
            return None

    def clear_buttons(self):
        self._queue.clear()

    def register_button_event_handler(self, callback, button=Button.BUTTON_1):
        pass

    def get_command(self):
        command = self._command
        self._command = None
        return command

    def test(self):
        pass

    def led_flash(self, led, period=0.2):

        # 10ms minimum flash speed
        if period < 0.010:
            period = 0.010

        self._leds[led].period = period

        if self._leds[led].state != UIBase.LED_State.LED_FLASH:
            self._leds[led].state = UIBase.LED_State.LED_FLASH
            self._do_flash(led)

    def led_on(self, led):
        self._leds[led].state = UIBase.LED_State.LED_ON
        self._set_led(led, UIBase.LED_State.LED_ON)

    def led_off(self, led):
        self._leds[led].state = UIBase.LED_State.LED_OFF
        self._set_led(led, UIBase.LED_State.LED_OFF)

    def _all_leds(self, state = LED_State.LED_OFF):
        if state == UIBase.LED_State.LED_OFF:
            self.led_off(Led.LED_RED)
            self.led_off(Led.LED_AMBER)
            self.led_off(Led.LED_GREEN)
        else:
            self.led_on(Led.LED_RED)
            self.led_on(Led.LED_AMBER)
            self.led_on(Led.LED_GREEN)

    def _set_led(self, led, state):
        pass

    # A handy method to show an crital error code upon failure
    def display_exception(self, error_code=1):
        self._all_leds(UIBase.LED_State.LED_OFF)

        while True:
            time.sleep(1)
            self._all_leds(UIBase.LED_State.LED_ON)
            time.sleep(1.25)
            self._all_leds(UIBase.LED_State.LED_OFF)
            time.sleep(0.5)

            for i in range(error_code):
                self._all_leds(UIBase.LED_State.LED_ON)
                time.sleep(0.25)
                self._all_leds(UIBase.LED_State.LED_OFF)
                time.sleep(0.25)

    def shutdown(self):
        # Shut everything down here before we exit

        if self._running:
            self._leds[Led.LED_GREEN].period = 0
            self.led_off(Led.LED_GREEN)

            self._leds[Led.LED_RED].period = 0
            self.led_off(Led.LED_RED)

            self._leds[Led.LED_AMBER].period = 0
            self.led_off(Led.LED_AMBER)

        self._running = False

def get_ui_instance():
    global _ui_instance
    if _is_raspberry_pi():
        import ZO.pi_ui

        if _ui_instance is None:
            _ui_instance = ZO.pi_ui.PI_UI()

    else:
        import ZO.pc_ui
        if _ui_instance is None:
            _ui_instance = ZO.pc_ui.PC_UI()

    return _ui_instance
