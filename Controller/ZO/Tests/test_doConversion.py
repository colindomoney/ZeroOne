import sys, os
from unittest import TestCase


from ZO import convert

class TestDoConversion(TestCase):
    def test_DoConversion(self):

        print('\n\n' + os.getcwd())
        convert.DoConversion('../../images/')
