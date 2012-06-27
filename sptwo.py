#!/usr/bin/python

def test_statistic_score(raw_data):
    norms = normalized(raw_data)
    ring = Ring(norms)
    test = StablePersistence(ring)
    test.run()
    return test.score()

# Stable Persistence classes

class StablePersistence:
    
    def __init__(self, ring, state=None):
        self.temps = sorted(ring.data)
        if not state:
            self.state = State(ring)
        else:
            self.state = state
        self.steps = len(self.temps)
    
    def run(self):
        while True:
            if not self._step():
                break
        self.state.cleanup()
        return
    
    def _step(self):
        if self.temps:
            self.steps -= 1
            self.state.raise_temp(self.temps.pop(0))
            return True
        else:
            return False
    
    def score(self):
        while self.steps > 0:
            self.run()
        
        pairs = self.state.pairs[:]
        perss = map(lambda (x,y): abs(x - y), pairs)
        pords = map(lambda x: x*x, perss)
        return sum(pords)

class State:
    
    def __init__(self, ring):
        self.ring = ring
        self.intervals = []
        self.pairs = []
        self.temp = None
    
    def cleanup(self):
        # This should only be called at the end of the run.
        ints = self.intervals
        if ints and len(ints) == 1 and self.temp == 1.0:
            if ints[0].birth == 0 and max(ints[0].values) == 1:
                self.intervals = []
                self.pairs.append( (0,1) )
            else:
                raise Exception("algorithm invariant violated")
        else:
            pass
    
    def raise_temp(self, temp):
        self.temp = temp
        includes = []
        
        for interval in self.intervals:
            # growth
            if interval.is_adjacent_to(temp):
                interval.assimilate(temp)
                includes.append(interval)
            else:
                pass
        
        if not includes:
            # births
            self.intervals.append(self.create_interval(temp))
            
        elif len(includes) == 1:
            # reality check
            if not temp in includes[0].values:
                raise Exception("this temp should have been included")
            
        elif len(includes) == 2:
            # deaths
            intA, intB = includes[0], includes[1]
            self.intervals.remove(intA)
            self.intervals.remove(intB)
            self.intervals.append(self.create_merged_interval(intA, intB))
            
        else:
            raise Exception("What in the world...")
        
    def do_collide(self, intA, intB):
        return intA.right == intB.left or intA.left == intB.right
    
    def create_interval(self, value):
        return Interval(value, value, value, self.ring)
    
    # N.B. This adds a min-max pairing to self.pairs!
    def create_merged_interval(self, intA, intB):
        if not self.do_collide(intA, intB):
            raise Exception("only colliding intervals can be merged")
        
        elif intA.right == intB.left:
            
            birth = min(intA.birth, intB.birth)
            left = intA.left
            right = intB.right

            pmin = max(intA.birth, intB.birth)
            pmax = intA.right # = intB.left
            
        elif intA.left == intB.right:
            
            birth = min(intA.birth, intB.birth)
            left = intB.left
            right = intA.right

            pmin = max(intA.birth, intB.birth)
            pmax = intB.right # = intA.left            
            
        else:
            raise Exception
        
        self.pairs.append( (pmin, pmax) )
        return Interval(birth, left, right, self.ring)

class Interval:
    
    def __init__(self, birth, left, right, ring):
        self.birth = birth
        self.left = left
        self.right = right
        self.ring = ring
        self.values = set([left, right])
        self.values |= set(ring.between(left, right))
    
    def is_adjacent_to(self, value):
        on_right = self._has_on_right(value)
        on_left = self._has_on_left(value)
        return on_right or on_left
    
    def _has_on_right(self, value):
        return self.ring.right_of(self.right) == value
    
    def _has_on_left(self, value):
        return self.ring.left_of(self.left) == value
    
    def assimilate(self, value):
        if not self.is_adjacent_to(value):
            raise Exception("cannot assimilate nonadjacent values")
        elif self._has_on_right(value):
            self.values.add(value)
            self.right = value
        elif self._has_on_left(value):
            self.values.add(value)
            self.left = value
        else:
            raise Exception
    
    def contains(self, value):
        return value in self.values

class Ring:
    
    def __init__(self, data):
        self.data = tuple(data)
        self.gmax = max(data)
        self.gmin = min(data)
    
    def left_of(self, value):
        if value in self.data:
            index = self.data.index(value)
            if index == 0:
                index = len(self.data) - 1
            else:
                index -= 1
            return self.data[index]
        else:
            return None
    
    def right_of(self, value):
        if value in self.data:
            index = self.data.index(value)
            if index == len(self.data) - 1:
                index = 0
            else:
                index += 1
            return self.data[index]
        else:
            return None
    
    def between(self, left, right):
        if not (left in self.data and right in self.data):
            raise Exception("invalid interval on ring")
        
        values = []
        trace = left
        
        while left != right:
            
            trace = self.right_of(trace)
            values.append(trace)
            
            # prevent writing right bound to list
            if self.left_of(right) == trace:
                break
        
        return values
    
    def is_max(self, value):
        if value == self.gmax:
            return True
        elif self.left_of(value) < value and self.right_of(value) < value:
            return True
        else:
            return False
    
    def is_min(self, value):
        if value == self.gmin:
            return True
        elif self.left_of(value) > value and self.right_of(value) > value:
            return True
        else:
            return False


# data processing functions

def normalized(data):
    count = len(data)
    ranks = ranked(data)
    if count <= 1:
        return None
    return map(lambda x: float(x-1)/float(count-1), ranks)

def ranked(data):
    sorts = sorted(data)
    return map(lambda x: sorts.index(x) + 1, data)


if __name__ == "__main__":
    print "This is a Stable Persistence module!"
