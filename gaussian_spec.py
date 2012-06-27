#!/usr/bin/python

import sys
import os.path
sys.path.append(os.path.dirname(__file__))
import gaussian as G
import unittest

TEST_N = 4
TEST_L = 19

class SeriesGeneratorTest(unittest.TestCase):
    
    def setUp(self):
        self.generator = G.SeriesGenerator()
    
    def test_generate(self):
        counter = 0
        for series in self.generator.generate(TEST_N, TEST_L):
            counter += 1
            self.assertEqual(len(series), TEST_L)
        else:
            self.assertEqual(TEST_N, counter)
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
