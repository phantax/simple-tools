#!/usr/bin/python

import sys
import os
from hashlib import sha256


#
# _____________________________________________________________________________
#
def accept(line, hashes, flagd):

    tokens = line.strip().split(':')
    if not tokens:
        return False

    myhex = tokens[0]
    if (len(myhex) % 2) != 0:
        return False

    if flagd:
        myhash = sha256(derandomize(myhex).decode("hex")).hexdigest()
    else:
        myhash = sha256(myhex.decode("hex")).hexdigest()

    if myhash in hashes:
        return False
    else:
        hashes.update([myhash])

    return True


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
    nAccepted = 0

    for fname in files:

        print(fname)

        nFileTotal = 0
        nFileAccepted = 0

        fAccepted = open(fname + '.accepted', 'w')
        fRejected = open(fname + '.rejected', 'w')

        if not fAccepted or not fRejected:
            print('Failed to write output file')
            continue

        for line in open(fname):
            nFileTotal += 1
            if accept(line, hashes, flagd):
                nFileAccepted += 1
                fAccepted.write(line)
            else:
                fRejected.write(line)

        print(' -> Total   : {0}'.format(nFileTotal))
        print(' -> Accepted: {0}'.format(nFileAccepted))
        print(' -> Rejected: {0}'.format(nFileTotal - nFileAccepted))

        nTotal += nFileTotal
        nAccepted += nFileAccepted

    print('Total   : {0}'.format(nTotal))
    print('Accepted: {0}'.format(nAccepted))
    print('Rejected: {0}'.format(nTotal - nAccepted))


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
        hexlist[i] = '0'

    return ''.join(hexlist)


#
# _____________________________________________________________________________
#
if __name__ == "__main__":
    main(sys.argv[1:])

