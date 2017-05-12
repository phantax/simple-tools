#!/usr/bin/python

import sys
import os
from hashlib import sha256

#
# _____________________________________________________________________________
#
def main(argv):

    if len(argv) < 1:
        return

    if argv[0] == '-d':
        flagd = True
        files = argv[1:]
    else:
        flagd = False
        files = argv

    hashes = set()

    nTotal = 0
    nUnique = 0
    nInvalid = 0

    for fname in files:

        print(fname)

        nFileTotal = 0
        nFileUnique = 0
        nFileInvalid = 0

        for line in open(fname):

            tokens = line.strip().split(':')
            if not tokens:
                continue
            myhex = tokens[0]
            myrest = ':'.join(tokens[1:])

            nFileTotal += 1

            if (len(myhex) % 2) != 0:
                nFileInvalid += 1
                continue

            if flagd:
                myhex = derandomize(myhex)

            myhash = sha256(myhex.decode("hex")).hexdigest()

            if myhash not in hashes:
                hashes.update([myhash])
                nFileUnique += 1

        print(' -> Total  : {0}'.format(nFileTotal))
        print(' -> Invalid: {0}'.format(nFileInvalid))

        nTotal += nFileTotal
        nUnique += nFileUnique
        nInvalid += nFileInvalid

    print('Total  : {0}'.format(nTotal))
    print('Unique : {0}'.format(nUnique))
    print('Invalid: {0}'.format(nInvalid))


#
# _____________________________________________________________________________
#
def derandomize(hexstr):

    if len(hexstr) < 12:
        return hexstr

    if hexstr[0:2] != "16":
        return hexstr

    if hexstr[10:12] != "01":
        return hexstr

    hexlist = list(hexstr)

    for i in range(22, 22 + min(len(hexstr) - 22, 64)):
        hexlist[i] = '{0:X}'.format(i - 22)[-1]

    return ''.join(hexlist)


#
# _____________________________________________________________________________
#
if __name__ == "__main__":
    main(sys.argv[1:])

