from collections import Iterable
from enum import Enum
from pynput.keyboard import Key, Listener
from blinkstick import blinkstick

from ZO.ui import UIBase, ButtonEvent, Commands


class PC_UI(UIBase):
    def __init__(self):
        self.__lastKey = None

        self.__keyboard = Keyboard_Driver(self.__on_press__, self.__on_release__)
        print('Keyboard created')
        self.__keyboard.register_key_event_handler(Keyboard_Driver.Keys.KEY1, self.__button_handler1)
        self.__keyboard.register_key_event_handler(Keyboard_Driver.Keys.KEY2, self.__button_handler2)
        self.__keyboard.register_key_event_handler(Keyboard_Driver.Keys.KEY3, self.__button_handler3)

    def __button_handler1(self, key, buttonEvent):
        print('__button_handler1() -> {}, {}'.format(key.value, buttonEvent))

    def __button_handler2(self, key, buttonEvent):
        print('__button_handler2() -> {}, {}'.format(key.value, buttonEvent))

    def __button_handler3(self, key, buttonEvent):
        print('__button_handler3() -> {}, {}'.format(key.value, buttonEvent))

    def __dir__(self):
        return super().__dir__()

    def __on_press__(self, key):
        # print('__on_press__')
        try:
            if key != self.__lastKey:
                self.__lastKey = key
                print('KEY = {0}'.format(key.char))
        except AttributeError:
            print('***')

    def __on_release__(self, key):
        # print('__on_release__')
        self.__lastKey = None

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

    def get_command(self):
        super().get_command()

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
    def register_key_event_handler(self, key, callback):
        self.keyHandler[key.value] = callback


class Blinkstick_LED_Driver():
    def __init__(self):
        pass
