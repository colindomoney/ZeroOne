import os, sys, collections
import time
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
        super().__init__()

        self._gpio = GPIO_Driver()

        self._gpio.register_key_event_handler(self._button_handler, Button.BUTTON_1)
        self._gpio.register_key_event_handler(self._button_handler, Button.BUTTON_2)
        self._gpio.register_key_event_handler(self._button_handler, Button.BUTTON_3)

        # TODO : This queue stuff can go in the base class really
        self._queue = collections.deque()

    def _button_handler(self, button, button_event):
        print('button_handler() -> {}, {}'.format(button.value, button_event))

        if button_event == ButtonEvent.BUTTON_UP:
            self._queue.appendleft(button)

    def get_button(self):
        if len(self._queue) != 0:
            return self._queue.pop()
        else:
            return None

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

    def test_button(self, button=Button.BUTTON_1):
        return self._gpio.test_button(button)

    def shutdown(self):
        super().shutdown()
        self._gpio.shutdown()

class GPIO_Driver():
    def __init__(self):
        self._platform = PiPlatform.ZeroOnePlatform
        self._gpioInitialised = False

        self._button_state = {
            Button.BUTTON_1: 0,
            Button.BUTTON_2: 0,
            Button.BUTTON_3: 0
        }

        self._button_handler = {
            Button.BUTTON_1: None,
            Button.BUTTON_2: None,
            Button.BUTTON_3: None,
        }

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
            GPIO.setwarnings(False)

            # Set the output pins
            GPIO.setup(17, GPIO.OUT)  # Red LED
            GPIO.setup(27, GPIO.OUT)  # Amber LED
            # The Green LED is hardwired to +5V

            # Set the input pins
            GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Outer Red button
            GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Middle Red button
            GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Black button

            # Set the initial values
            GPIO.output(17, 1)
            GPIO.output(27, 1)

            GPIO.add_event_detect(2, GPIO.BOTH, callback=self._button_callback)
            GPIO.add_event_detect(3, GPIO.BOTH, callback=self._button_callback)
            GPIO.add_event_detect(22, GPIO.BOTH, callback=self._button_callback)

        else:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)

            # Set the output pins
            GPIO.setup(17, GPIO.OUT)  # Green LED
            GPIO.setup(27, GPIO.OUT)  # Red LED

            # Set the input pins
            GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Black button
            GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Red button

            # Set the initial values
            GPIO.output(17, 1)
            GPIO.output(27, 1)

            GPIO.add_event_detect(2, GPIO.BOTH, callback=self._button_callback)
            GPIO.add_event_detect(3, GPIO.BOTH, callback=self._button_callback)

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

    def test_button(self, button=Button.BUTTON_1):
        return self._button_state[button]

    def _button_callback(self, pin):
        time.sleep(.05)

        # print(pin)

        if pin == 2:
            button = Button.BUTTON_1
        elif pin == 3:
            button = Button.BUTTON_2
        else:
            button = Button.BUTTON_3


        if (GPIO.input(pin) != 0 and self._button_state[button] != 0):
            # print("<U>")
            self._button_state[button] = 0
            if self._button_handler[button] != None:
                self._button_handler[button](button, ButtonEvent.BUTTON_UP)
        elif (GPIO.input(pin) == 0 and self._button_state[button] == 0):
            # print("<D>")
            if self._button_handler[button] != None:
                self._button_handler[button](button, ButtonEvent.BUTTON_DOWN)
            self._button_state[button] = 1

    # Register a callback method to register for the events
    def register_key_event_handler(self, callback, button=Button.BUTTON_1):
        self._button_handler[button] = callback

    def shutdown(self):
        self._gpioInitialised = False
        GPIO.cleanup()