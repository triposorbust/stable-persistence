#!/usr/bin/python

import random

class SeriesGenerator:
    def __init__(self):
        pass
    def generate(self, n=10, l=12):
        for i in range(n):
            yield self._make_series(l)
    def _make_series(self, length=12):
        mu = 20 * (random.random() - 0.5)
        sd = 5 * random.random()
        return [random.gauss(mu, sd) for x in range(length)]

if __name__ == '__main__':
    for i in range(100000):
        print random.gauss(0,5.0)
