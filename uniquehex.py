#!/usr/bin/python

import sys
import os

#
# _____________________________________________________________________________
#
def main(argv):

    hashes = set()

    N = 0

    for fname in argv:

        abspath = os.path.abspath(fname)

        dataset = abspath.split('/')[-3]

        for line in open(abspath):
            (myid, myhash) = line.split(':')[:2]
            N += 1
 
            myhash = myhash.strip()

            if myhash not in hashes:
                hashes.update([myhash])
                fullid = dataset + ':' + myid.split('~')[0]
                print(fullid)

#    print('Found {0} stimuli ({1} unique)'.format(N, len(hashes)))


#
# _____________________________________________________________________________
#
if __name__ == "__main__":
    main(sys.argv[1:])

