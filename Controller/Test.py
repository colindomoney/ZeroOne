import sys
import threading
import time
from enum import Enum
from ZO import zero_one

from getkey import getkey, keys
from pynput.keyboard import Key, Listener


# import sys
# sys.path.append('./pydev')
# from pydev import pydevd
# pydevd.settrace('localhost', port=51234, stdoutToServer=True, stderrToServer=True)


def toggle_led():
    print(". ")
    global timer
    timer = threading.Timer(1, toggle_led)
    timer.start()


def main1():
    # toggle_led()

    try:
        print('Running main')
        cnt = 0

        while True:
            time.sleep(0.2)
            print('x')
            time.sleep(0.2)

            cnt = cnt + 1
            # if (cnt > 4):
            #     timer.cancel()

    except KeyboardInterrupt:
        print("Exiting")
        # timer.cancel()


def main2():
    def on_press(key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(key):
        print('{0} released'.format(
            key))
        if key == Key.esc:
            # Stop listener
            return False

    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


def main3():
    key = getkey()
    buffer = ''
    if key == keys.UP:
        pass
    elif key == keys.DOWN:
        pass
    else:  # Handle text characters
        buffer += key
        print(buffer)


def main4():
    print('in main()')

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
                    return item.name
            return None

    v1 = ['q' == item.value for item in Keys]

    print(v1)


def main_logging():
    import logging

    def setup_logging():
        print("setup_logging")

        logging.basicConfig(
            format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
            handlers=[
                logging.FileHandler("./zero_one.log"),
                logging.StreamHandler(sys.stdout)
            ])

        global log
        log = logging.getLogger('zero_one')
        log.setLevel(logging.INFO)

    def destroy_logging():
        print("destroy_logging")

    setup_logging()

    log.info('info')

    destroy_logging()


ZERO_ONE_MASK_FILE = '/Users/colind/Projects/ZeroOne/ZeroOne/Controller/ZO/zero_one.npy'
IMAGE_FILE = '/Users/colind/Projects/ZeroOne/ZeroOne/Graphics/Images/RGBW.png'


def main_graphics():
    from PIL import Image
    import numpy
    from ZO import image

    print('main_graphics')

    # Open the file, get the data and convert it to a list
    imgData = list(Image.open(IMAGE_FILE).getdata())

    # Get the mask data, flatten it out and convert it to a list
    # maskData = list(numpy.load(ZERO_ONE_MASK_FILE).flatten())

    maskData = image.load_mask_data()

    # Zip the data
    combinedData = list(zip(imgData, maskData))

    # Get everything that isn't a zero in the mask
    outputFrame = [x[0] for x in combinedData if x[1] != 0]

    # TODO : Test the length here
    if len(outputFrame) != zero_one.ZO_PIXEL_COUNT:
        raise zero_one.ZeroOneException('Pixel count not the expected length after masking')

        # Create a NumPy array, which has four elements. The top-left should be pure red, the top-right should be pure blue, the bottom-left should be pure green, and the bottom-right should be yellow
    # pixels = numpy.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 0]]])

    # Create a PIL image from the NumPy array
    # image = Image.fromarray(pixels.astype('uint8'), 'RGB')

    # Save the image
    # image.show()


def main():
    # xvals = list(range(1, 39))
    # yvals = list(range(1, 29))

    # import pylibftdi as ftdi
    # bb = ftdi.BitBangDevice(device_id='123')

    import FtdiGpio as FtdiGpio

    with FtdiGpio.FtdiGpio() as ftgp:
        ftgp.set_direction(0)


    print('Done')


if __name__ == "__main__":
    # main_graphics()
    main()
