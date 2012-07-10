#!/usr/bin/python

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__),"src"))

import parsed as P
import gaussian as G
import sptwo as SP

TEST_N = 1000
P_VALUE = 0.01
AVERAGED = False

def main(filename):
    gauss = G.SeriesGenerator()
    parsed = P.SeriesIterator(filename, AVERAGED)
    
    if AVERAGED:
        PD_LEN = len(set([v for v in parsed.pattern if v != None]))
    else:
        PD_LEN = len([v for v in parsed.pattern if v != None])

    null_distribution = []
    for series in gauss.generate(TEST_N, PD_LEN):
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
        
        if (len(data) <= 1) or (len(set(data[:])) < len(data)):
            continue
        
        score = SP.test_statistic_score(data)
        n = len(filter(lambda x: x <= score, null_distribution))
        
        # print "%s\t%s\t%s" % (name, str(score), str(float(n)/float(N)))
        
        total += 1
        if float(n)/float(N) < P_VALUE:
            significant += 1
        
        # END ITERATION
        
    fraction = float(significant)/float(total)
    # print "n.d. parms:\tN=%d\tL=%d" % (TEST_N, PD_LEN)
    print "%s\tP=%.3f\t%d\t%f" % (filename, P_VALUE, significant, fraction)

    return

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        main(sys.argv[1])
    else:
        main("sine.data")
