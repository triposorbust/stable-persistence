#!/usr/bin/python

import os.path
import sys
sys.path.append(os.path.dirname(__file__))
import parser as P
import unittest

TEST_FILENAME = "parser.spec"

class SeriesIteratorTest(unittest.TestCase):
    def setUp(self):
        self.iterator = P.SeriesIterator(TEST_FILENAME)
    
    def test_iteration(self):
        counter = 0
        for series in self.iterator:
            counter += 1
            for number in series:
                self.assertIsInstance(number, float)
            self.assertEqual(counter, len(series))
        else:
            self.assertEqual(counter, 12)
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

