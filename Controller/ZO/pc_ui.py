from collections import Iterable
from enum import Enum
from pynput.keyboard import Key, Listener
from blinkstick import blinkstick

from ZO.ui import UIBase, ButtonEvent, Commands


class PC_UI(UIBase):
    def __init__(self):
        super().__init__()

        self._lastKey = None

        self.__keyboard = Keyboard_Driver(self._on_press, self._on_release)
        print('Keyboard created')
        self.__keyboard.register_key_event_handler(super().button_handler1, Keyboard_Driver.Keys.KEY1)
        self.__keyboard.register_key_event_handler(super().button_handler2, Keyboard_Driver.Keys.KEY2)
        self.__keyboard.register_key_event_handler(super().button_handler3, Keyboard_Driver.Keys.KEY3)

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

    def led_on(self, Led):
        super().led_on(Led)

    def led_off(self, Led):
        super().led_off(Led)

    def led_flash(self, Led, period=500):
        super().led_flash(Led, period)

    def test_button(self, Button=UIBase.Button.BUTTON_1):
        super().test_button(Button)

    def register_button_event_handler(self, callback, Button=UIBase.Button.BUTTON_1):
        super().register_button_event_handler(callback, Button)

    def test(self):
        self.__keyboard.test()


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
        print('Keyboard_Driver.__init__()')

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

        #     global timer
        #     timer = threading.Timer(1, toggle_led)
        #     timer.start()

        # Setup the timers

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
    def __init__(self):
        pass
