#!/usr/bin/python

import sys
import glob


#
#____________________________________________________________________________________
#

def issue(filename, iLine, description):
    print('\033[1;31m-> {0}#{1:08}: {2}\033[0m'.format(filename, iLine, description))


#
#____________________________________________________________________________________
#

def sanitize(filename):

    iLine = 0
    for line in open(filename):
        iLine += 1

        tokens = line.strip().split(':')

        if len(tokens) == 0:
            issue(filename, iLine, 'Empty line')
            continue

        myhex = tokens[0]
        if len(myhex) == 0:
            issue(filename, iLine, 'Empty hex string')
            continue

        if (len(myhex) % 2) != 0:
            issue(filename, iLine, 'Odd hex length')
            continue

        try:
            myhex.decode("hex")
        except:
            issue(filename, iLine, 'Invalid hex string')
            continue


#
#____________________________________________________________________________________
#

def main(argv):

    for pattern in argv:
        files = sorted(glob.glob(pattern))
        for filename in files:
            print('Sanitizing "{0}" ...'.format(filename))
            sanitize(filename)



#
# _____________________________________________________________________________
#
if __name__ == "__main__":
    main(sys.argv[1:])
