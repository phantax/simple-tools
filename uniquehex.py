#!/usr/bin/python

import sys
import os
from hashlib import sha256

#
# _____________________________________________________________________________
#
def main(argv):

    files = argv

    hashes = set()

    N = 0
    n = 0
    X = 0

    for fname in files:

        for line in open(fname):

            tokens = line.strip().split(':')
            if not tokens:
                continue
            myhex = tokens[0]
            myrest = ':'.join(tokens[1:])

            N += 1

            if (len(myhex) % 2) != 0:
                X += 1
                continue

            myhash = sha256(myhex.decode("hex")).hexdigest()

            if myhash not in hashes:
                hashes.update([myhash])
                n += 1

    print(N)
    print(n)
    print(X)

#
# _____________________________________________________________________________
#
if __name__ == "__main__":
    main(sys.argv[1:])

