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

    for i, arg in enumerate(argv):
        if not arg.startswith('-'):
            argFileIndex = i
            break   

    args = argv[:argFileIndex]
    files = argv[argFileIndex:]
    hashes = set()

    flagd = '-d' in args    # use de-randomization?
    flago = '-o' in args    # write output files?

    nTotal = 0
    nAccepted = 0

    for fname in files:

        print(fname)

        nFileTotal = 0
        nFileAccepted = 0

        fAccepted = None
        fRejected = None
        if flago:
            fNameAccepted = fname + '.accepted'
            if os.path.isfile(fNameAccepted):
                print(' ->| already exists: ' + fNameAccepted)
            else:
                fAccepted = open(fNameAccepted, 'w')
                print(' => ' + fNameAccepted)

            fNameRejected = fname + '.rejected'
            if os.path.isfile(fNameRejected):
                print(' ->| already exists: ' + fNameRejected)
            else:
                fRejected = open(fNameRejected, 'w')
                print(' => ' + fNameRejected)

        for line in open(fname):
            nFileTotal += 1
            if accept(line, hashes, flagd):
                nFileAccepted += 1
                if fAccepted is not None:                
                    fAccepted.write(line)
            else:
                if fRejected is not None:           
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

