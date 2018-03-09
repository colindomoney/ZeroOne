import os
import sys
from enum import Enum

from blinkstick import blinkstick
from pynput.keyboard import Key, Listener

from ZO.ui import UIBase, ButtonEvent, Led
from ZO.zero_one import ZeroOneException


class PC_UI(UIBase):
    def __init__(self):
        super().__init__()

        self._lastKey = None

        # Create the keyvoard driver
        self.__keyboard = Keyboard_Driver(self._on_press, self._on_release)
        self.__keyboard.register_key_event_handler(super().button_handler1, Keyboard_Driver.Keys.KEY1)
        self.__keyboard.register_key_event_handler(super().button_handler2, Keyboard_Driver.Keys.KEY2)
        self.__keyboard.register_key_event_handler(super().button_handler3, Keyboard_Driver.Keys.KEY3)

        # Create the BlinkStick driver
        self.__blinkstick = Blinkstick_LED_Driver()


    def _on_press(self, key):
        # print('__on_press__')
        if key != self._lastKey:
            self._lastKey = key

            try:
                super().process_keystroke(key.char)
            except AttributeError:
                if key == Key.esc:
                    super().process_keystroke(0x1c)
                elif key == Key.space:
                        super().process_keystroke(0x20)

    def _on_release(self, key):
        # print('__on_release__')
        self._lastKey = None

    def led_on(self, led):
        super().led_on(led)
        self.__blinkstick.led_on(led)

    def led_off(self, led):
        super().led_off(led)
        self.__blinkstick.led_off(led)

    # Don't do this in the derived class
    # def led_flash(self, led, period=500):
    #     super().led_flash(led, period)

    def test(self):
        pass

# noinspection PyCallingNonCallable
class Keyboard_Driver():
    class Keys(Enum):
        KEY1 = 'q'
        KEY2 = 'w'
        KEY3 = 'e'

        @classmethod
        def contains(cls, key):
            return any(key == item.value for item in cls)

        @classmethod
        def byvalue(cls, val):
            for item in cls:
                if item.value == val:
                    return item
            return None

    def __init__(self, on_press, on_release):
        # Check if we're on a Mac here, and see if we have GUID; if not throw an exception
        if sys.platform == 'darwin':
              if os.getuid() != 0:
                  raise ZeroOneException("Must be run as root on a Mac, use 'sudo -s '")

        # Store the last_key_press
        self.keyEvents = {
            self.Keys.KEY1.value: None,
            self.Keys.KEY2.value: None,
            self.Keys.KEY3.value: None,
        }

        self.keyHandler = {
            self.Keys.KEY1.value: None,
            self.Keys.KEY2.value: None,
            self.Keys.KEY3.value: None,
        }

        # Setup the hook functions
        self.listener = Listener(
            on_press=self.__on_press__,
            on_release=self.__on_release__)

        self.listener.start()
        self.listener.wait()

        self.__client_on_press = on_press
        self.__client_on_release = on_release


    def __on_press__(self, key):
        try:
            ch = key.char

            if not self.Keys.contains(ch):
                self.__client_on_press(key)
            else:
                if self.keyEvents[ch] != ButtonEvent.BUTTON_DOWN:
                    self.keyEvents[ch] = ButtonEvent.BUTTON_DOWN
                    if self.keyHandler[ch] != None:
                        self.keyHandler[ch](self.Keys.byvalue(ch), ButtonEvent.BUTTON_DOWN)

            # print('Key = {0}'.format(ch))
        except AttributeError:
            self.__client_on_press(key)

    # noinspection PyCallingNonCallable
    def __on_release__(self, key):
        # Make s
        try:
            ch = key.char

            if not self.Keys.contains(ch):
                self.__client_on_release(key)
            else:
                if self.keyEvents[ch] != ButtonEvent.BUTTON_UP:
                    self.keyEvents[ch] = ButtonEvent.BUTTON_UP
                    if self.keyHandler[ch] != None:
                        self.keyHandler[ch](self.Keys.byvalue(ch), ButtonEvent.BUTTON_UP)

        except AttributeError:
            self.__client_on_release(key)

    def test(self):
        pass

    # Register a callback method to register for the events
    def register_key_event_handler(self, callback, key = Keys.KEY1):
        self.keyHandler[key.value] = callback

class Blinkstick_LED_Driver():
    class LED(Enum):
        Led1 = 1,
        Led2 = 2,
        Led3 = 3

    def __init__(self):
        # Check the hardware is present
        self._stick = blinkstick.find_by_serial('BS015264-2.2')
        if self._stick == None:
            raise ZeroOneException("Unable to find BlinkStick, is it plugged in?")

        self._stick.set_error_reporting(False)

        mode = self._stick.get_mode()
        if mode == None:
            raise ZeroOneException("BlinkStick is not set to mode 2, we're fucked")

        # Put the LEDs off
        self.led_off(Led.LED_RED)
        self.led_off(Led.LED_GREEN)

    # TODO : put all the clever stuff in here
    def set_led(self, led, state):
        pass

    def led_off(self, led):
        if led == Led.LED_GREEN:
            self._stick.set_color(0, 0, name='black')

        if led == Led.LED_RED:
            self._stick.set_color(1, 0, name='black')

    def led_on(self, led):
        if led == Led.LED_GREEN:
            self._stick.set_color(0, 0, name='green')

        if led == Led.LED_RED:
            self._stick.set_color(1, 0, name='red')
