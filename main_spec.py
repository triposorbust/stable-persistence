#!/usr/bin/python

import sys
import os.path
sys.path.append(os.path.dirname(__file__))
import main as M
import unittest

class MainTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
