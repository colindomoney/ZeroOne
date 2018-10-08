import fnmatch
import inspect, itertools
import time, pprint
import psutil, sys, os, signal
from PIL import Image
from ZO.zero_one import MoreSillyStuff, ZeroOneException


# A class to contain the control of the screen effects ie. a base class, animations, etc

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class BaseEffect():
    def __init__(self):
        pass

    # Methods
    # start
    # stop

    # Properties
    # Name
    # Description
    # Author
    # Duration
    # Continuous (R/W)
    # isBusy

class SillyStuff(BaseEffect):
    def __init__(self):
        print('SillyStuff():__init__()')

from itertools import chain

def subclasses(cls):
    return list(
        chain.from_iterable(
            [list(chain.from_iterable([[x], subclasses(x)])) for x in cls.__subclasses__()]
        )
    )

class EffectController(metaclass=Singleton):
    def __init__(self):
        pass

    def test(self, opt):
        print('test()', opt)

def inherits_from(child, parent_name):
    if inspect.isclass(child):
        if parent_name in [c.__name__ for c in inspect.getmro(child)[1:]]:
            return True
    return False

class ImageCycler():
    def __init__(self, path):
        self._images = []
        self._path = path

        if os.path.exists(path) == False:
            raise ZeroOneException('Path does not exist in ImageCycler()')

        self._build_image_list()

        self._iterable_images = itertools.cycle(self._images)

    def _build_image_list(self):
        patterns = ['*.png', '*.jpg']

        self._images = []
        for p in patterns:
            self._images.append(fnmatch.filter(os.listdir(self._path), p))

        # Flatten the list of lists
        self._images =  [val for sublist in self._images for val in sublist]

    def get_next_file(self):
        base_filename = next(self._iterable_images)
        return(os.path.join(self._path, base_filename))


if __name__ == '__main__':
    ec = EffectController()

    res = subclasses(BaseEffect)
    print(res)

    from importlib import import_module

    # cls = getattr(import_module('__main__'), 'SillyStuff')
    # print(cls, SillyStuff)
    # cls()

    cls = getattr(import_module('ZO.zero_one'), 'MoreSillyStuff')
    print(cls, SillyStuff)
    cls()

    print(issubclass(cls, BaseEffect))