import sys, os
from unittest import TestCase

from ZO import convert

# TODO: Setup and teardown scripts
# TODO: Setup - checks the directory exists
# TODO: Teardown - removes all superflous files

class TestDoConversion(TestCase):

    @classmethod
    def setUp(cls):
        pass
        # print('\nsetUp()')

    @classmethod
    def setUpClass(cls):
        # Set the image directory and check it exists
        cls.IMAGE_DIRECTORY = '../../images/'
        if os.path.exists(cls.IMAGE_DIRECTORY) == False:
            raise FileNotFoundError('Image directory not found')

    @classmethod
    def tearDownClass(self):
        self.DeleteAllConvertedFiles()

    @classmethod
    def DeleteAllConvertedFiles(cls):
        # Delete all the converted images
        for f in cls.GetConvertedFiles(cls.IMAGE_DIRECTORY):
            os.remove(cls.IMAGE_DIRECTORY  + f)

    @classmethod
    def GetConvertedFiles(cls, input):
        return [ x for x in os.listdir(input) if os.path.splitext(x)[0].endswith('_zo')]

    def test_DoConversion(self):
        # self.DeleteAllConvertedFiles(self)
        self.DeleteAllConvertedFiles()

        # print('\n\n' + os.getcwd())
        # convert.DoConversion(self.IMAGE_DIRECTORY)

    def test_DoIRun(self):
        res = self.GetConvertedFiles(self.IMAGE_DIRECTORY)
        print(len(res))