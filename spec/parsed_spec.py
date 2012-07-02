#!/usr/bin/python

import os.path
import sys
sys.path.append(os.path.relpath("../src", os.path.dirname(__file__)))
import parsed as P
import unittest

TEST_FILENAME = "parsed.spec"

class AcceptanceTest(unittest.TestCase):
    def setUp(self):
        self.parser = P.SeriesIterator(TEST_FILENAME)
    
    def test_data_parsing_a(self):
        self.parser.parse_pattern("# Z2 Z4 Z3 Z1")
        ud = [1.0, None, 2.0, 4.0]
        pd = self.parser.pattern_series(ud)
        self.assertEqual([4.0, 1.0, 2.0], pd)
    
    def test_data_parsing_b(self):
        self.parser.parse_pattern("# Z0 Z2 Z4 Z6 Z0 Z2 Z4 Z6")
        ud = [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7]
        pd = self.parser.pattern_series(ud)
        self.assertEqual([2.2, 3.3, 4.4, 5.5], pd)
    
    def test_data_parsing_c(self):
        self.parser.parse_pattern("# FOOZ1 FOOZ4 FOOZ1 FOOZ6")
        ud = [3.14, 0.0, 1.1, 4.1]
        pd = self.parser.pattern_series(ud)
        self.assertEqual([2.12, 0.0, 4.1], pd)
    
    def tearDown(self):
        pass

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
    
    def test_zstr_to_t(self):
        self.assertEqual(self.iterator.zstr_to_t("CerianiZT12"), 12)
        self.assertEqual(self.iterator.zstr_to_t("Z0"), 0)
        self.assertEqual(self.iterator.zstr_to_t("ChangZT20"), 20)
        self.assertEqual(self.iterator.zstr_to_t("UedaZT1"), 1)
        self.assertEqual(self.iterator.zstr_to_t("#"), None)
        self.assertEqual(self.iterator.zstr_to_t("FOO"), None)
    
    def test_parse_pattern(self):
        self.assertIsInstance(self.iterator.pattern, tuple)
        self.iterator.parse_pattern("# FOO 12 Z12 0 4 Z8 BAR4")
        self.assertEqual(self.iterator.pattern, (None, 12, 12, 0, 4,8,4))
        self.iterator.parse_pattern("#")
        self.assertEqual(self.iterator.pattern, ())
    
    def test_vstr_to_v(self):
        self.assertEqual(self.iterator.vstr_to_v("3.3"), 3.3)
        self.assertEqual(self.iterator.vstr_to_v("NA"), None)
        self.assertEqual(self.iterator.vstr_to_v("-1"), -1.0)
    
    def test_pattern_series(self):
        self.iterator.pattern = None
        self.assertEqual(self.iterator.pattern_series("foobar"), "foobar")
        
        self.iterator.pattern = (1, None, 3, 2, 1)
        ud = map(float, range(5))
        pd = self.iterator.pattern_series(ud)
        self.assertEqual(pd, [2.0, 3.0, 2.0])
        
        self.iterator.pattern = (4, 3, None, 3)
        ud = [4.0, 1.0, 3.0, 2.0]
        pd = self.iterator.pattern_series(ud)
        self.assertEqual(pd, [1.5, 4.0])

        self.iterator.pattern = None
        ud = [1, "FOO"]
        pd = self.iterator.pattern_series(ud)
        self.assertEqual(pd, [1, "FOO"])
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

