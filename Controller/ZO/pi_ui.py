import os, sys
from enum import Enum

from ZO.ui import UIBase, ButtonEvent, Led, Button
from ZO.zero_one import ZeroOneException

try:
    import RPi.GPIO as GPIO
except ImportError:
    raise ZeroOneException("Failed to import RPi.GPIO, are you running on a Pi?")

class PiPlatform(Enum):
    DebugPlaform = 0
    ZeroOnePlatform = 1

class PI_UI(UIBase):
    def __init__(self):
        print('PI_UI::__init__()')

        super().__init__()

        self._gpio = GPIO_Driver()

    def led_flash(self, led, period=0.2):
        super().led_flash(led, period)

    def led_on(self, led):
        super().led_on(led)
        self._set_led(led, UIBase.LED_State.LED_ON)

    def led_off(self, led):
        super().led_off(led)
        self._set_led(led, UIBase.LED_State.LED_OFF)

    def _set_led(self, led, state):
        """ This function is a low level method that just drives the LED without changing the actual state of internal variables """
        if state == UIBase.LED_State.LED_ON:
            self._gpio.led_on(led)
        else:
            self._gpio.led_off(led)

    def shutdown(self):
        print('shutdown()')
        super().shutdown()

        self._gpio.shutdown()

class GPIO_Driver():
    def __init__(self):
        self._platform = PiPlatform.ZeroOnePlatform
        self._gpioInitialised = False

        # A horrible hack here to determine if we're running on 01 hardware or a test Pi
        # Look for a file called 'debug_platform' in the root of the install folder
        this_directory = os.path.dirname(os.path.realpath(__file__))

        # Get to the Controller/ZO directory then drop back one level
        if os.path.exists(os.path.join(this_directory, '../debug_platform')):
            print('Running on DEBUG PLATFORM')
            self._platform = PiPlatform.DebugPlaform
        else:
            print('Running on ZERO_ONE PLATFORM')

        # Setup the GPIO here
        if self._platform == PiPlatform.ZeroOnePlatform:
            GPIO.setmode(GPIO.BCM)

            # Set the output pins
            GPIO.setup(17, GPIO.OUT)  #  LED
            GPIO.setup(27, GPIO.OUT)  #  LED

            # Set the input pins
            GPIO.setup(2, GPIO.IN)  # Black button
            GPIO.setup(3, GPIO.IN)  # Red button

            # Set the initial values
            GPIO.output(17, 1)
            GPIO.output(27, 1)
        else:
            GPIO.setmode(GPIO.BCM)

            # Set the output pins
            GPIO.setup(17, GPIO.OUT)  # Green LED
            GPIO.setup(27, GPIO.OUT)  # Red LED

            # Set the input pins
            GPIO.setup(2, GPIO.IN)  # Black button
            GPIO.setup(3, GPIO.IN)  # Red button

            # Set the initial values
            GPIO.output(17, 1)
            GPIO.output(27, 1)

        self._gpioInitialised = True

    def led_on(self, led):
        if self._gpioInitialised:
            if self._platform == PiPlatform.ZeroOnePlatform:
                if led == Led.LED_RED:
                    GPIO.output(17, 0)
                elif led == Led.LED_AMBER:
                    GPIO.output(27, 0)
            else:
                if led == Led.LED_GREEN:
                    GPIO.output(17, 0)
                elif led == Led.LED_RED:
                    GPIO.output(27, 0)

    def led_off(self, led):
        if self._gpioInitialised:
            if self._platform == PiPlatform.ZeroOnePlatform:
                if led == Led.LED_RED:
                    GPIO.output(17, 1)
                elif led == Led.LED_AMBER:
                    GPIO.output(27, 1)
            else:
                if led == Led.LED_GREEN:
                    GPIO.output(17, 1)
                elif led == Led.LED_RED:
                    GPIO.output(27, 1)

    def shutdown(self):
        self._gpioInitialised = False
        GPIO.cleanup()


# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17, GPIO.OUT)  # Green LED
# GPIO.setup(27, GPIO.OUT)  # Red LED
# GPIO.setup(2, GPIO.IN)  # Black button
# GPIO.setup(3, GPIO.IN)  # Red button

# For the ZeroOne I guess:

# 2 = Black
# 3 = Red1
# 4 = Red2
# 17 = Red LED
# 27 = Amber LED
# 22 = Green LED