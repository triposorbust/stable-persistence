#!/usr/bin/python

import os.path
import sys
sys.path.append(os.path.relpath("../src", os.path.dirname(__file__)))
import parsed as P
import unittest

TEST_FILENAME = "parsed.spec"

class CatAcceptanceTest(unittest.TestCase):
    def setUp(self):
        self.cat_parser = P.SeriesIterator(TEST_FILENAME, False)
    
    def test_data_parsing_a(self):
        self.cat_parser.parse_pattern("# ZT2 ZT3 ZT1")
        ud = [1.0, None, 2.0]
        pd = self.cat_parser.pattern_series(ud)
        self.assertEqual([2.0, 1.0], pd)
    
    def test_data_parsing_b(self):
        self.cat_parser.parse_pattern("# Z0 Z0 Z2 Z2 Z4 Z4 Z6 Z6")
        ud = [x*2 for x in range(8)]
        pd = self.cat_parser.pattern_series(ud)
        self.assertEqual([0, 4, 8, 12, 2, 6, 10, 14], pd)
    
    def test_data_parsing_c(self):
        self.cat_parser.parse_pattern("# FOOZ1 FOOZ3 FOOZ2 FOOZ1")
        ud = [3.14, 0.0, 1.1, 4.1]
        pd = self.cat_parser.pattern_series(ud)
        self.assertEqual([3.14, 1.1, 0.0, 4.1], pd)
    
    def tearDown(self):
        pass

class AvgAcceptanceTest(unittest.TestCase):
    def setUp(self):
        self.avg_parser = P.SeriesIterator(TEST_FILENAME, True)
    
    def test_data_parsing_a(self):
        self.avg_parser.parse_pattern("# Z2 Z4 Z3 Z1")
        ud = [1.0, None, 2.0, 4.0]
        pd = self.avg_parser.pattern_series(ud)
        self.assertEqual([4.0, 1.0, 2.0], pd)
    
    def test_data_parsing_b(self):
        self.avg_parser.parse_pattern("# Z0 Z2 Z4 Z6 Z0 Z2 Z4 Z6")
        ud = [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7]
        pd = self.avg_parser.pattern_series(ud)
        self.assertEqual([2.2, 3.3, 4.4, 5.5], pd)
    
    def test_data_parsing_c(self):
        self.avg_parser.parse_pattern("# FOOZ1 FOOZ4 FOOZ1 FOOZ6")
        ud = [3.14, 0.0, 1.1, 4.1]
        pd = self.avg_parser.pattern_series(ud)
        self.assertEqual([2.12, 0.0, 4.1], pd)
    
    def tearDown(self):
        pass

class SeriesIteratorTest(unittest.TestCase):
    def setUp(self):
        self.avg_parser = P.SeriesIterator(TEST_FILENAME, True)
        self.cat_parser = P.SeriesIterator(TEST_FILENAME, False)
    
    def _test_iteration_helper(self, parser):
        counter = 0
        for series in parser:
            self.assertTrue(series[0]) # should be a string
            counter += 1
            for number in series[1]:
                self.assertIsInstance(number, float)
            self.assertEqual(counter, len(series[1]))
        else:
            self.assertEqual(counter, 12)
    
    def test_iteration(self):
        self._test_iteration_helper(self.avg_parser)
        self._test_iteration_helper(self.cat_parser)
    
    def _test_zstr_to_t_helper(self, parser):
        self.assertEqual(parser.zstr_to_t("CerianiZT12"), 12)
        self.assertEqual(parser.zstr_to_t("Z0"), 0)
        self.assertEqual(parser.zstr_to_t("ChangZT20"), 20)
        self.assertEqual(parser.zstr_to_t("UedaZT1"), 1)
        self.assertEqual(parser.zstr_to_t("#"), None)
        self.assertEqual(parser.zstr_to_t("FOO"), None)        
    
    def test_zstr_to_t(self):
        self._test_zstr_to_t_helper(self.avg_parser)
        self._test_zstr_to_t_helper(self.cat_parser)
    
    def _test_parse_pattern_helper(self, parser):
        self.assertIsInstance(parser.pattern, tuple)
        parser.parse_pattern("# FOO 12 Z12 0 4 Z8 BAR4")
        self.assertEqual(parser.pattern, (None, 12, 12, 0, 4, 8, 4))
        parser.parse_pattern("#")
        self.assertEqual(parser.pattern, ())        
    
    def test_parse_pattern(self):
        self._test_parse_pattern_helper(self.avg_parser)
        self._test_parse_pattern_helper(self.cat_parser)
    
    def _test_vstr_to_v_helper(self, parser):
        self.assertEqual(parser.vstr_to_v("3.3"), 3.3)
        self.assertEqual(parser.vstr_to_v("NA"), None)
        self.assertEqual(parser.vstr_to_v("-1"), -1.0)        
    
    def test_vstr_to_v(self):
        self._test_vstr_to_v_helper(self.avg_parser)
        self._test_vstr_to_v_helper(self.cat_parser)
    
    def _test_pattern_series_helper(self, parser):
        parser.pattern = None
        self.assertEqual(parser.pattern_series("foobar"), "foobar")
        
    
    def test_cat_pattern_series(self):
        self._test_pattern_series_helper(self.cat_parser)
        
        self.cat_parser.pattern = (None, 1, 1, 1, 2, 3)
        ud = map(float, range(6))
        pd = self.cat_parser.pattern_series(ud)
        self.assertEqual(pd, [1.0, 4.0, 5.0, 2.0, 3.0])
        
        self.cat_parser.pattern = (4, 3, 3, 2, 2, 1, 1, 1)
        ud = map(float, range(8))
        ud.reverse()
        pd = self.cat_parser.pattern_series(ud)
        self.assertEqual(pd, [2.0, 4.0, 6.0, 7.0, 1.0, 3.0, 5.0, 0.0])
        
        self.cat_parser.pattern = None
        ud = [1, "FOO"]
        pd = self.cat_parser.pattern_series(ud)
        self.assertEqual(pd, [1, "FOO"])
    
    def test_avg_pattern_series(self):
        self._test_pattern_series_helper(self.avg_parser)
        
        self.avg_parser.pattern = (1, None, 3, 2, 1)
        ud = map(float, range(5))
        pd = self.avg_parser.pattern_series(ud)
        self.assertEqual(pd, [2.0, 3.0, 2.0])
        
        self.avg_parser.pattern = (4, 3, None, 3)
        ud = [4.0, 1.0, 3.0, 2.0]
        pd = self.avg_parser.pattern_series(ud)
        self.assertEqual(pd, [1.5, 4.0])

        self.avg_parser.pattern = None
        ud = [1, "FOO"]
        pd = self.avg_parser.pattern_series(ud)
        self.assertEqual(pd, [1, "FOO"])
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

