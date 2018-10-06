import os, sys
from enum import Enum

from blinkstick import blinkstick
from pynput.keyboard import Key, Listener

from ZO.ui import UIBase, ButtonEvent, Led, Button
from ZO.zero_one import ZeroOneException


class PC_UI(UIBase):
    def __init__(self):
        super().__init__()

        self._buttonEvents = {
            Button.BUTTON_1.value: None,
            Button.BUTTON_2.value: None,
            Button.BUTTON_3.value: None,
        }

        self._lastKey = None

        # Create the keyvoard driver
        self._keyboard = Keyboard_Driver(self._on_press, self._on_release)
        self._keyboard.register_key_event_handler(self._button_handler, Keyboard_Driver.Keys.KEY1)
        self._keyboard.register_key_event_handler(self._button_handler, Keyboard_Driver.Keys.KEY2)
        self._keyboard.register_key_event_handler(self._button_handler, Keyboard_Driver.Keys.KEY3)

        # Create the BlinkStick driver
        self._blinkstick = Blinkstick_LED_Driver()

    def _on_press(self, key):
        # print('__on_press__ : {0}'.format(key))
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
        # print('__on_release__ : {0}'.format(key))
        self._lastKey = None

    def _button_handler(self, key, button_event):
        print('button_handler1() -> {}, {}'.format(key.value, button_event))

        if key.value == Keyboard_Driver.Keys.KEY1.value:
            self._buttonEvents[Button.BUTTON_1.value] = button_event;
            if button_event == ButtonEvent.BUTTON_UP:
                self._queue.appendleft(Button.BUTTON_1)

        if key.value == Keyboard_Driver.Keys.KEY2.value:
            self._buttonEvents[Button.BUTTON_2.value] = button_event;
            if button_event == ButtonEvent.BUTTON_UP:
                self._queue.appendleft(Button.BUTTON_2)

        if key.value == Keyboard_Driver.Keys.KEY3.value:
            self._buttonEvents[Button.BUTTON_3.value] = button_event;
            if button_event == ButtonEvent.BUTTON_UP:
                self._queue.appendleft(Button.BUTTON_3)

    def led_on(self, led):
        super().led_on(led)
        self._set_led(led, UIBase.LED_State.LED_ON)

    def led_off(self, led):
        super().led_off(led)
        self._set_led(led, UIBase.LED_State.LED_OFF)

    def _set_led(self, led, state):
        """ This function is a low level method that just drives the LED without changing the actual state of internal variables """
        if state == UIBase.LED_State.LED_ON:
            self._blinkstick.led_on(led)
        else:
            self._blinkstick.led_off(led)

    def test_button(self, button=Button.BUTTON_1):
        if self._buttonEvents[button.value] == ButtonEvent.BUTTON_DOWN:
            return True
        else:
            return False

    def test(self):
        pass


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

    def __on_release__(self, key):
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

    # Register a callback method to register for the events
    def register_key_event_handler(self, callback, key=Keys.KEY1):
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

    def led_off(self, led):
        if led == Led.LED_GREEN:
            self._stick.set_color(1, 0, name='black')

        if led == Led.LED_RED:
            self._stick.set_color(0, 0, name='black')

        if led == Led.LED_AMBER:
            self._stick.set_color(2, 0, name='black')

    def led_on(self, led):
        brightness = 24

        if led == Led.LED_GREEN:
            # self._stick.set_color(0, 0, name='green')
            self._stick.set_color(1, 0, red=0, green=brightness, blue=0)

        if led == Led.LED_RED:
            # self._stick.set_color(1, 0, name='red')
            self._stick.set_color(0, 0, red=brightness, green=0, blue=0)

        if led == Led.LED_AMBER:
            # self._stick.set_color(0, 0, name='green')
            self._stick.set_color(2, 0, red=brightness, green=brightness, blue=0)
