#!/usr/bin/python

import string
import sys

class SeriesIterator:
    def __init__(self, filename="default.data"):
        self.filename = filename
        try:
            self._file = open(filename, "rU")
            self._file.readline() # throw away first line
        except IOError as e:
            raise e
    def __iter__(self):
        return self
    def next(self):
        str = self._file.readline()
        if not str:
            raise StopIteration
        words = string.split(str)
        series_name = words[0]
        series_data = map(float, words[1:])
        return (series_name, series_data)

if __name__ == '__main__':
    print "This is a parser module."
