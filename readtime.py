#!/usr/bin/python

import sys
import glob
import datetime


#
#____________________________________________________________________________________
#

def getTimestamp(line):

    args = line.split(':')[-1]

    tsStr = (s for s in args.split(';')
            if s.startswith('T=') or s.startswith('time=')).next()

    dt = datetime.datetime.strptime(tsStr.split('=')[1], '%Y%m%d-%H%M%S')

    return dt

#
#____________________________________________________________________________________
#

def getFirstAndLastLine(filename):

    first = None
    last = None

    n = 0
    for line in open(filename):
        if first is None:
            first = line.strip()
        last = line.strip()
        n += 1
        
    return first, last, n


#
#____________________________________________________________________________________
#

def main(argv):

    rates = []

    for pattern in argv:
        files = sorted(glob.glob(pattern))
        for filename in files:
            print('Analyzing "{0}" ...'.format(filename))
            first, last, n = getFirstAndLastLine(filename)

            dtFirst = getTimestamp(first)
            dtLast = getTimestamp(last)

            rate = float(n) / (dtLast - dtFirst).seconds
            rates += [rate]

            print('  -> {0:3.1f} ops/s'.format(rate))
            
    if len(rates) > 0:
        print('Average = {0:3.1f} ops/s'.format(sum(rates) / len(rates)))
    

#
# _____________________________________________________________________________
#
if __name__ == "__main__":
    main(sys.argv[1:])
