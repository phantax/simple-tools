#!/usr/bin/python

import sys
import os


#
# _____________________________________________________________________________
#
def usage():

    print('Usage: ./uniquehex.py [OPTIONS] INPUT-FILE FILTER-FILE')


#
# _____________________________________________________________________________
#
def main(argv):

    argFileIndex = 0
    for i, arg in enumerate(argv):
        if not arg.startswith('-'):
            argFileIndex = i
            break   

    args = argv[:argFileIndex]
    files = argv[argFileIndex:]

    if len(files) < 2:
        usage()
        return

    fInName = files[0]
    fFilterName = files[1]
    fOutName = fInName + '.filtered'

    print('    in: {0}'.format(fInName))
    print('filter: {0}'.format(fFilterName))
    print('   out: {0}'.format(fInName))

    fOut = None
    if os.path.isfile(fOutName):
        print(' ->| already exists: ' + fOutName)
    else:
        fOut = open(fOutName, 'w')
        print(' => ' + fOutName)

    fIn = open(fInName)
    fFilter = open(fFilterName)

    nTotal = 0
    nAccepted = 0

    nextLine = None

    iLine = 0
    for line in fIn:

        # Keep track of line numbers
        iLine += 1

        nTotal += 1

        if nextLine is None:
            filterLine = fFilter.readline()
            if filterLine:
                nextLine = int(filterLine.split('#')[1])
            else:
                nextLine = None

        if iLine != nextLine:
            continue

        nextLine = None
        nAccepted += 1

        if fOut is not None:
            fOut.write(line)

    print(' -> Total   : {0}'.format(nTotal))
    print(' -> Accepted: {0}'.format(nAccepted))
    print(' -> Rejected: {0}'.format(nTotal - nAccepted))


#
# _____________________________________________________________________________
#
if __name__ == "__main__":
    main(sys.argv[1:])

