#!/usr/bin/python

import string
import sys

class SeriesIterator:
    def __init__(self, filename="default.data"):
        self.filename = filename
        self.pattern = None
        try:
            self._file = open(filename, "rU")
            self.parse_pattern(self._file.readline())
        except IOError as e:
            raise e
    
    def parse_pattern(self, pattern_string):
        pattern = string.split(pattern_string)
        if (not pattern) or (pattern[0] != "#"):
            raise Exception("unexpected data format")
        uniques = list(set(pattern[1:]))
        
        # assume that all replicates are blocked.
        counts = map(lambda x: pattern.count(x), uniques)
        self.pattern = tuple(counts)
    
    def __iter__(self):
        return self
    
    def pattern_series(self, unpatterned):
        if not self.pattern:
            return filter(lambda x: x or x == 0, unpatterned)
        elif len(unpatterned) != sum(self.pattern):
            raise Exception("poorly patterned data series")
        patterned = []
        for n in self.pattern:
            values = filter(lambda x: x or x == 0, unpatterned[0:n])
            del unpatterned[0:n]
            patterned.append(float(sum(values)) / float(len(values)))
        return patterned
    
    def transform_string(self, string):
        try:
            return float(string)
        except ValueError:
            return None
    
    def next(self):
        str = self._file.readline()
        if not str:
            raise StopIteration
        words = string.split(str)
        unpatterned = map(self.transform_string, words[1:])
        
        series_name = words[0]
        series_data = self.pattern_series(unpatterned)
        return (series_name, series_data)


if __name__ == '__main__':
    print "This is a parser module."
