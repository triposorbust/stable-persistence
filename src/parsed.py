#!/usr/bin/python

import string
import re

class SeriesIterator:
    def __init__(self, filename="default.data", averaged=False):
        self.filename = filename
        self.pattern = None
        self.averaged = averaged
        try:
            self._file = open(filename, "rU")
            self.parse_pattern(self._file.readline())
        except IOError as e:
            raise e
    
    def parse_pattern(self, pattern_string):
        zstrs = string.split(pattern_string)
        if (not zstrs) or (zstrs[0] != "#"):
            raise Exception("unexpected data format")        
        self.pattern = tuple(map(self.zstr_to_t, zstrs[1:]))
    
    def _averaged_series(self, unpatterned):
        ts = list(set(filter(lambda x: x or x == 0, list(self.pattern))))
        td = dict(zip(ts, [[] for x in ts]))
        
        for i,n in enumerate(unpatterned):
            time = self.pattern[i]
            if n != None and time in td.keys():
                td[time].append(n)
            continue
        
        times = sorted(td.keys())
        bundles = filter(lambda x: x!=[], map(lambda t: td[t], times))
        averages = map(lambda vs: sum(vs)/len(vs), bundles)
        
        return averages        
    
    def _concatenated_series(self, unpatterned):
        labels = list(self.pattern)
        if len(labels) != len(unpatterned):
            raise Exception("badly formed data series")
        zipped = zip(labels, unpatterned)
        
        ts = sorted(filter(lambda x: x or x == 0, list(set(labels[:]))))
        gets = lambda t: [(l,d) for (l,d) in zipped[:] if l==t]
        bundles = map(gets, ts)
        
        concatenated = []
        imax = max([len(l) for l in bundles])
        for i in range(imax):
            for bundle in bundles:
                if len(bundle) > i and bundle[i][1] != None:
                    t,v = bundle[i]
                    concatenated.append(v)
                else:
                    pass
        return concatenated
    
    def pattern_series(self, unpatterned):
        if (not self.pattern):
            return filter(lambda x: x != None, unpatterned)
        elif self.averaged:
            return self._averaged_series(unpatterned)
        else:
            return self._concatenated_series(unpatterned)
    
    def zstr_to_t(self, word):
        m = re.search(r"[\d]{1,2}$",word)
        if not m:
            return None
        return int(m.group())
    
    def vstr_to_v(self, string):
        try:
            return float(string)
        except ValueError:
            return None
    
    
    def __iter__(self):
        return self
        
    def next(self):
        astr = self._file.readline()
        if not astr:
            raise StopIteration
        words = string.split(astr)
        
        if self.pattern and len(words) - 1 != len(self.pattern):
            raise Exception("poorly patterned data series")

        unpatterned = map(self.vstr_to_v, words[1:])
        
        name = words[0]
        data = self.pattern_series(unpatterned)
        return (name, data)


if __name__ == '__main__':
    print "This is a parser module."
