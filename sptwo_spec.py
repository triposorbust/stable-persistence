#!/usr/bin/python

import sys
import os.path
sys.path.append(os.path.dirname(__file__))
import sptwo as SP
import unittest
import random

TEST_N = 12

class MockState:
    def __init__(self):
        self.ring = MockRing()
        self.temps_count = 0
        self.pairs = zip(reversed(range(TEST_N)), range(TEST_N))
    def raise_temp(self, temp):
        self.temps_count += 1
    def cleanup(self):
        pass

class StablePersistenceTest(unittest.TestCase):
    
    def setUp(self):
        self.m_state = MockState()
        self.sp = SP.StablePersistence(MockRing(), self.m_state)
    
    def test_temps(self):        
        self.assertEqual(len(self.sp.temps), len(range(TEST_N)))
        sorts = sorted(range(TEST_N))
        for i in sorts:
            self.assertIn(i, self.sp.temps)
            self.assertEqual(sorts.index(i), self.sp.temps.index(i))
    
    def test_steps(self):
        self.assertEqual(self.sp.steps, TEST_N)
    
    def test_run(self):
        self.sp.run()
        self.assertEqual(self.m_state.temps_count, TEST_N)
        self.assertEqual(self.sp.steps, 0)
    
    def test_score(self):
        # see mock above for test pairs
        sq_odds = [x*x for x in range(TEST_N) if x % 2 == 1]
        expect = 2 * sum(sq_odds)
        self.assertEqual(self.sp.score(), expect)
    
    def tearDown(self):
        pass

class MockInterval:
    def __init__(self, birth, left, right):
        self.values = [birth, left, right]
        self.birth = birth
        self.left = left
        self.right = right
    def is_adjacent_to(self, value):
        return abs(self.left - value) == 1 or abs(self.right - value) == 1
    def assimilate(self, value):
        if abs(self.left - value) == 1:
            self.left = value
            self.values.append(value)
        elif abs(self.right - value) == 1:
            self.right = value
            self.values.append(value)
        else:
            return

class StateStepTest(unittest.TestCase):
    
    def setUp(self):
        self.m_intA = MockInterval(-1, 2, 4)
        self.m_intB = MockInterval(4, 6, 7)
        self.m_intC = MockInterval(-101, -101, -101)
        self.state = SP.State(MockRing())
        self.state.intervals = [self.m_intA, self.m_intB, self.m_intC]
    
    def test_raise_temp_assimilations(self):
        self.state.raise_temp(8)
        self.assertEqual(len(self.state.intervals), 3)
        self.assertEqual(self.m_intB.right, 8)
        self.assertEqual(len(self.state.pairs), 0)
    
    def test_raise_temp_births(self):
        self.state.raise_temp(202)
        self.assertEqual(len(self.state.intervals), 4)
    
    def test_raise_temp_deaths(self):
        self.state.raise_temp(5)
        
        self.assertNotIn(self.m_intA, self.state.intervals)
        self.assertNotIn(self.m_intB, self.state.intervals)
        self.assertIn(self.m_intC, self.state.intervals)
        
        self.assertEqual(len(self.state.intervals), 2)
        
        self.assertEqual(self.state.intervals[1].birth, -1)
        self.assertEqual(self.state.intervals[1].left, 2)
        self.assertEqual(self.state.intervals[1].right, 7)
        
    def test_raise_temp_pairs(self):
        self.assertFalse(self.state.pairs)
        self.assertEqual(self.state.pairs, [])
        
        self.state.raise_temp(5)
        
        self.assertTrue(self.state.pairs)
        self.assertEqual(self.state.pairs[0], (4, 5))
    
    def tearDown(self):
        pass

class StateTest(unittest.TestCase):
    
    def setUp(self):
        self.state = SP.State(MockRing())
    
    def test_cleanup(self):
        self.state.intervals.append(MockInterval(0, 1, 1))
        self.assertEqual(len(self.state.intervals), 1)
        self.assertEqual(self.state.pairs, [])
        self.state.temp = 1.0 # raised temp to 1.0
        self.state.cleanup()
        self.assertEqual(len(self.state.pairs), 1)
        self.assertEqual(self.state.intervals, [])
        self.assertEqual(self.state.pairs[0], (0,1))
        
    def test_create_interval(self):
        new_interval = self.state.create_interval(101)
        self.assertEqual(new_interval.birth, 101)
        self.assertEqual(new_interval.left, 101)
        self.assertEqual(new_interval.right, 101)
        self.assertTrue(isinstance(new_interval, SP.Interval))
    
    def test_do_collide(self):
        m_intA = MockInterval(0, -2, 2)
        m_intB = MockInterval(0, 2, 6)
        m_intC = MockInterval(0, -6, -2)
        
        self.assertTrue(self.state.do_collide(m_intA, m_intB))
        self.assertTrue(self.state.do_collide(m_intA, m_intC))
        self.assertFalse(self.state.do_collide(m_intB, m_intC))
    
    def test_create_merged_interval(self):
        m_intA = MockInterval(-10, -2, 2)
        m_intB = MockInterval(0, 2, 6)
        
        self.assertEqual(len(self.state.pairs), 0)
        
        intC = self.state.create_merged_interval(m_intA, m_intB)
        
        self.assertEqual(len(self.state.pairs), 1)
        self.assertEqual(self.state.pairs[0], (0, 2))
        
        self.assertTrue(isinstance(intC, SP.Interval))
        self.assertEqual(intC.birth, -10)
        self.assertEqual(intC.left, -2)
        self.assertEqual(intC.right, 6)
    
    def tearDown(self):
        pass

class MockRing:
    def __init__(self):
        self.data = tuple(range(TEST_N))
        self.gmin = -97
        self.gmax = 98
    def left_of(self, value):
        return value - 3
    def right_of(self, value):
        return value + 3
    def between(self, left, right):
        big = max(left, right)
        small = min(left, right)
        return range(small + 1, big)

class IntervalTest(unittest.TestCase):
    
    def setUp(self):
        self.m_ring = MockRing();
        self.small = SP.Interval(0, 0, 0, self.m_ring)
        self.large = SP.Interval(3, 3, 7, self.m_ring)
    
    def test_values(self):
        pass
    
    def test_is_adjacent_to(self):
        
        self.assertTrue(self.small.is_adjacent_to(-3))
        self.assertTrue(self.small.is_adjacent_to(3))
        self.assertTrue(self.large.is_adjacent_to(0))
        self.assertTrue(self.large.is_adjacent_to(10))
        
        self.assertFalse(self.large.is_adjacent_to(5))
        self.assertFalse(self.large.is_adjacent_to(100))
    
    def test_assimilate(self):
        
        self.assertEqual(self.small.left, 0)
        self.assertEqual(self.small.right, 0)
        self.assertNotIn(-3, self.small.values)
        
        self.small.assimilate(-3)
        
        self.assertEqual(self.small.left, -3)
        self.assertEqual(self.small.right, 0)
        self.assertIn(-3, self.small.values)
        
        
        self.assertEqual(self.large.left, 3)
        self.assertEqual(self.large.right, 7)
        self.assertNotIn(10, self.large.values)
        
        self.large.assimilate(10)
        
        self.assertEqual(self.large.left, 3)
        self.assertEqual(self.large.right, 10)
        self.assertIn(10, self.large.values)

    def test_contains(self):
        
        self.assertTrue(self.small.contains(0))
        self.assertFalse(self.small.contains(1))
        
        self.assertTrue(self.large.contains(3))
        self.assertTrue(self.large.contains(5))
        self.assertFalse(self.large.contains(10))
    
    def tearDown(self):
        pass

class RingTest(unittest.TestCase):
    
    def setUp(self):
        self.flat = SP.Ring(range(TEST_N))
        self.crests = SP.Ring([x*(-1)**x for x in range(TEST_N)])
    
    def test_gmax(self):
        self.assertEqual(self.flat.gmax, TEST_N - 1)
    def test_gmin(self):
        self.assertEqual(self.flat.gmin, 0)
    
    def test_left_of(self):
        self.assertIsNone(self.flat.left_of(TEST_N))
        self.assertEqual(self.flat.left_of(2), 1)
        self.assertEqual(self.flat.left_of(0), TEST_N - 1)
    
    def test_right_of(self):
        self.assertEqual(self.flat.right_of(-1), None)
        self.assertEqual(self.flat.right_of(1), 2)
        self.assertEqual(self.flat.right_of(TEST_N - 1), 0)
    
    def test_between(self):
        self.assertEqual(self.flat.between(0, 0), [])
        self.assertEqual(self.crests.between(2, 2), [])
        self.assertEqual(self.flat.between(3, 5), [4])
        self.assertEqual(self.crests.between(2, -7), [-3,4,-5,6])
    
    def test_is_max(self):
        self.assertTrue(self.flat.is_max(11))
        self.assertFalse(self.flat.is_max(10))
        maxvals = filter(lambda x: x > 0, self.crests.data)
        minvals = filter(lambda x: x < 0, self.crests.data)
        for val in maxvals:
            self.assertTrue(self.crests.is_max(val))
        for val in minvals:
            self.assertFalse(self.crests.is_max(val))
    
    def test_is_min(self):
        self.assertTrue(self.flat.is_min(0))
        self.assertFalse(self.flat.is_min(1))
        maxvals = filter(lambda x: x > 0, self.crests.data)
        minvals = filter(lambda x: x < 0, self.crests.data)
        for val in maxvals:
            self.assertFalse(self.crests.is_min(val))
        for val in minvals:
            self.assertTrue(self.crests.is_min(val))
    
    def tearDown(self):
        pass

class DataProcessingTest(unittest.TestCase):
    
    def test_ranked(self):
        # ranks should be 1-index, not zero-index.
        
        test_straight = range(TEST_N)
        rstraight = SP.ranked(map(lambda x: 2*x, test_straight))
        rreverse = SP.ranked(map(lambda x: 2*x, reversed(test_straight)))
        
        for (x,y) in zip(rstraight, test_straight):
            self.assertEqual(x, y + 1)
        for (x,y) in zip(rreverse, reversed(test_straight)):
            self.assertEqual(x, y + 1)
    
    def test_normalized(self):
        test = [10*random.random() for x in range(TEST_N)]
        norm = SP.normalized(test)
        for n in norm:
            self.assertTrue(n <= 1)
            self.assertTrue(n >= 0)
        self.assertEqual(len(norm), len(set(norm)))


if __name__ == '__main__':
    unittest.main()
