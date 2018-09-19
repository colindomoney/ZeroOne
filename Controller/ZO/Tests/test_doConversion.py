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

    @classmethod
    def setUpClass(cls):
        # Set the image directory and check it exists
        cls.ImageDirectory = '../../images/'
        cls.NumberOfFiles = 5
        if os.path.exists(cls.ImageDirectory) == False:
            raise FileNotFoundError('Image directory not found')

    @classmethod
    def tearDownClass(self):
        self.DeleteAllConvertedFiles()

    @classmethod
    def DeleteAllConvertedFiles(cls):
        # Delete all the converted images
        for f in cls.GetConvertedFiles(cls.ImageDirectory):
            os.remove(cls.ImageDirectory  + f)

    @classmethod
    def GetConvertedFiles(cls, input):
        return [ x for x in os.listdir(input) if os.path.splitext(x)[0].endswith('_zo')]

    def test_DoConversion(self):
        # Clean all the files to start with
        self.DeleteAllConvertedFiles()

        # Count the converted files, should be zero
        self.assertEqual(0, len(self.GetConvertedFiles(self.ImageDirectory)))

        # Count the input files, should be 5
        self.assertEqual(self.NumberOfFiles, len(os.listdir(self.ImageDirectory)))

        # Now convert the directory

        # Count the converted files, should be 5

        # Now check all the files are the right size

    def test_DoIRun(self):
        res = self.GetConvertedFiles(self.ImageDirectory)
        print(len(res))