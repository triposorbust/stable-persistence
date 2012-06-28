#!/usr/bin/python

import sys
import os.path
sys.path.append(os.path.dirname(__file__))

import parser as P
import gaussian as G
import sptwo as SP

TEST_N = 100
TEST_L = 12
P_VALUE = 0.01

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
    
    significant = 0
    total = 0
    fraction = 0.0
    
    for series in parsed:
        
        name = series[0]
        data = series[1]
        if len(set(data[:])) < len(data): # sp does not handle duplicates.
            continue
        
        score = SP.test_statistic_score(data)
        n = len(filter(lambda x: x <= score, null_distribution))
        #
        # print "%s\t%s\t%s" % (name, str(score), str(float(n)/float(N)))
        #
        total += 1
        if float(n)/float(N) < P_VALUE:
            significant += 1
        
        # END ITERATION
        
    fraction = float(significant)/float(total)
    print "%s\tN=%d\tP=%.3f\t%f" % (filename, TEST_N, P_VALUE, fraction)

    return

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        main(sys.argv[1])
    else:
        main("sine.data")
