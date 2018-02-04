
import io
from enum import Enum

def __is_raspberry_pi__(raise_on_errors=False):
    """Checks if Raspberry PI.

    :return:
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

__ui_instance__ = None

class ButtonEvent(Enum):
    BUTTON_DOWN = 1
    BUTTON_UP = 2

class UIBase:
    class Button(Enum):
        BUTTON_1 = 1
        BUTTON_2 = 2
        BUTTON_3 = 3

    class Led(Enum):
        LED_RED = 1
        LED_GREEN = 2

    def __init__(self):
        pass

    def led_on(self, Led):
        pass

    def led_off(self, Led):
        pass

    def led_flash(self, Led, period=500):
        pass

    def test_button(self, Button = Button.BUTTON_1):
        pass

    def register_button_event_handler(self, callback, Button = Button.BUTTON_1):
        pass

    def test(self):
        pass

def get_ui_instance():
    global __ui_instance__
    if __is_raspberry_pi__():
        import ZO.pi_ui
        # if __un_instance__ == None:
            # __un_instance__ = ZO

    else:
        import ZO.pc_ui
        if __ui_instance__ == None:
            __ui_instance__ = ZO.pc_ui.PC_UI()

    return __ui_instance__