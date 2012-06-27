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
            self.assertTrue(series[0]) # should be a string
            counter += 1
            for number in series[1]:
                self.assertIsInstance(number, float)
            self.assertEqual(counter, len(series[1]))
        else:
            self.assertEqual(counter, 12)
    
    def test_parse_pattern(self):
        self.iterator.parse_pattern("# A A A B B C C C C D E")
        self.assertEqual(self.iterator.pattern, (3,4,2,1,1))
        self.iterator.parse_pattern("# 0 2 4 6 8 10 12 14 16 18 20 22")
        expect = tuple([1 for x in range(12)])
        self.assertEqual(self.iterator.pattern, expect)
    
    def test_pattern_series(self):
        self.iterator.pattern = None
        self.assertEqual(self.iterator.pattern_series("foobar"), "foobar")
        
        self.iterator.pattern = (2,2,2)
        ud = range(6)
        pd = self.iterator.pattern_series(ud)
        self.assertEqual(pd, [0.5, 2.5, 4.5])
        
        self.iterator.pattern = (4,3,2)
        ud = range(9)
        ud.reverse()
        pd = self.iterator.pattern_series(ud)
        self.assertEqual(pd, [6.5, 3, 0.5])
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

