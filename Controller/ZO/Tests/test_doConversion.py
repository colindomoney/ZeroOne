import sys, os
from unittest import TestCase

from ZO import convert

# TODO: Setup and teardown scripts
# TODO: Setup - checks the directory exists
# TODO: Teardown - removes all superflous files

class TestDoConversion(TestCase):

    @classmethod
    def setUp(self):
        pass
        # print('\nsetUp()')

    @classmethod
    def setUpClass(self):
        # print('\nsetUpClass()')

        # Set the image directory and check it exists
        self.IMAGE_DIRECTORY = '../../images/'
        if os.path.exists(self.IMAGE_DIRECTORY) == False:
            raise FileNotFoundError('Image directory not found')

        self.numbers = [1, 6, 3, 8, 4, 9]

    @classmethod
    def tearDownClass(self):
        for f in self.GetConvertedFiles(self, self.IMAGE_DIRECTORY):
            os.remove(self.IMAGE_DIRECTORY  + f)

    def test_DoConversion(self):
        pass

        # print('\n\n' + os.getcwd())
        # convert.DoConversion(self.IMAGE_DIRECTORY)

    def GetConvertedFiles(self, input):
        return [ x for x in os.listdir(input) if os.path.splitext(x)[0].endswith('_zo')]

    def test_DoIRun(self):
        res = self.GetConvertedFiles(self.IMAGE_DIRECTORY)
        print(len(res))