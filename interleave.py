#!/usr/bin/python

import sys
import os


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

    linesfiles = [[line.strip() for line in open(filename)] for filename in files]

    maxlines = max([len(lines) for lines in linesfiles])

    for i in range(maxlines):
        for j in range(len(linesfiles)):
            if i < len(linesfiles[j]):            
                print(linesfiles[j][i])


#
# _____________________________________________________________________________
#
if __name__ == "__main__":
    main(sys.argv[1:])

