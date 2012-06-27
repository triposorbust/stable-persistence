#!/usr/bin/python

import sys
import os.path
sys.path.append(os.path.dirname(__file__))

import parser as P
import gaussian as G
import sptwo as SP

TEST_N = 100
TEST_L = 12

def main(filename):
    gauss = G.SeriesGenerator()
    parsed = P.SeriesIterator(filename)
    
    null_distribution = []
    for series in gauss.generate(TEST_N, TEST_L):
        score = SP.test_statistic_score(series)
        null_distribution.append(score)
    else:
        null_distribution.sort()
    
    N = TEST_N
    n = 0
    
    for series in parsed:
        name = series[0]
        score = SP.test_statistic_score(series[1])
        n = len(filter(lambda x: x <= score, null_distribution))
        print "%s\t%s\t%s" % (name, str(score), str(float(n)/float(N)))

    return

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        main(sys.argv[1])
    else:
        main("sine.data")
