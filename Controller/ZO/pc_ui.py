from collections import Iterable
from enum import Enum
from pynput.keyboard import Key, Listener
from blinkstick import blinkstick

from ZO.ui import UIBase

class PC_UI(UIBase):
    def __init__(self):
        self.__keyboard = Keyboard_Driver()
        print('Keyboard created')
        self.__keyboard.register_key_event_handler(Keyboard_Driver.Keys.KEY1, self.__button_handler)

    def __button_handler(self, key):
        print('__button_handler() -> ' + key)

    def __dir__(self):
        return super().__dir__()

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
        KEY1 = '1'
        KEY2 = '2'
        KEY3 = '3'

    def __init__(self):
        print('Keyboard_Driver.__init__()')

        # Store the last_key_press
        self.keyEvents = {
            self.Keys.KEY1: None,
            self.Keys.KEY2: None,
            self.Keys.KEY3: None,
        }

        # Setup the hook functions
        self.listener = Listener(
                on_press = self.__on_press__,
                on_release = self.__on_release__)

        self.listener.start()
        self.listener.wait()

        #     global timer
        #     timer = threading.Timer(1, toggle_led)
        #     timer.start()

        # Setup the timers

    def __on_press__(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def __on_release__(self, key):
        print('{0} released'.format(
            key))


    def test(self):
        print('Running = ' + str(self.listener.running))

    # Register a callback method to register for the events
    def register_key_event_handler(self, key, callback):
        self.keyEvents[key] = callback

class Blinkstick_LED_Driver():
    def __init__(self):
        pass
