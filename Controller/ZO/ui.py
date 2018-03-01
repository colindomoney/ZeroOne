import io
from enum import Enum
import kbhit


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


if __is_raspberry_pi__() == False:
    from pynput.keyboard import Key, Listener


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


    class CommandProcessor():
        def __init__(self):
            self.__lastCommand = None
            self.__kb = kbhit.KBHit()
            # self.__kb.set_normal_term()

        #     # Setup the hook functions
        #     self.listener = Listener(
        #         on_press=self.__on_press__,
        #         on_release=self.__on_release__)
        #
        #     self.listener.start()
        #     self.listener.wait()
        #
        # def __on_press__(self, key):
        #     try:
        #         if key == Key.esc:
        #             self.__lastCommand = Commands.Quit
        #             print(' got ESC ')
        #     except AttributeError:
        #         raise
        #
        # def __on_release__(self, key):
        #     # Don't need to do anything with the release event
        #     try:
        #         pass
        #     except AttributeError:
        #         raise

        def get_command(self):
            while self.__kb.kbhit():
                c = self.__kb.getch()

                print('c = {0}'.format(hex(ord(c))))

                # while self.__kb.kbhit():
                #     self.__kb.getch()

                # if ord(c) == 27:
                #     return Commands.Quit

            return None

        def shutdown(self):
            self.__kb.set_normal_term()

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
        self._command = None
        pass

    def button_handler1(self, key, buttonEvent):
        print('button_handler1() -> {}, {}'.format(key.value, buttonEvent))

    def button_handler2(self, key, buttonEvent):
        print('button_handler2() -> {}, {}'.format(key.value, buttonEvent))

    def button_handler3(self, key, buttonEvent):
        print('button_handler3() -> {}, {}'.format(key.value, buttonEvent))

    def process_keystroke(self, key):
        print('< {} >'.format(key))

        if key == 0x1c:
            self._command = Commands.Quit

    def led_on(self, Led):
        pass

    def led_off(self, Led):
        pass

    def led_flash(self, Led, period=500):
        pass

    def test_button(self, Button=Button.BUTTON_1):
        pass

    def register_button_event_handler(self, callback, Button=Button.BUTTON_1):
        pass

    def get_command(self):
        command = self._command
        self._command = None
        return command

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
