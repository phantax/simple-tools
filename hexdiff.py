#!/usr/bin/python

import sys


#
# _____________________________________________________________________________
#
def main(argv):

    if len(argv) != 2:
        print('Invalid number of arguments')
        return

    a = hextobin(argv[0])
    b = hextobin(argv[1])

    if a is None or b is None:
        print('Input strings have invalid length')
        return

    print('lvd = {0}'.format(levenshtein(a, b)))


#
# _____________________________________________________________________________
#
def hextobin(hexstr):
    if (len(hexstr) % 2) != 0:
        return None
    return [int(hexstr[i:i+2], base=16) for i in range(0, len(hexstr), 2)]


#
# _____________________________________________________________________________
#
def colorize(elements, colorMap={}):

    # Make a copy of the list of elements
    coloredElements = [e for e in elements]

    # Apply color
    for color, indices in colorMap.iteritems():
        for i in indices:    
            coloredElements[i] = '\033[1;{0}m{1}\033[0m' \
                    .format(color, coloredElements[i])                            

    return coloredElements


#
# _____________________________________________________________________________
#
def tableize(hexlist):

    lines = [' '.join(hexlist[i:i+16]) for i in range(0, len(hexlist), 16)]
    return '\n'.join(lines)


#
# _____________________________________________________________________________
#
def levenshtein(a, b):

    d = getMatrix(a, b)
    path = getOptimalPath(d)


    la = 0
    lb = 0

    B = [x for x in a]

    listIns = []
    listDels = []
    listSubsa = []
    listSubsb = []

    print('='*20)

    ia, ib = 0, 0
    for da, db in path:                           

        if da == 1 and db == 1:
            if d[ia][ib] != d[ia+1][ib+1]:
                print('[{2}] Sub {0:02X} -> {1:02X}'.format(a[ia], b[ib], ia + lb))
                listSubsa.append(ia)
                listSubsb.append(ib)
                B[ia + lb] = b[ib]
        elif db == 1:
            print('[{1}] Ins {0:02X}'.format(b[ib], ib))
            listIns.append(ib)
            B.insert(ib, b[ib])
            lb += 1
        elif da == 1:
            print('[{1}] Del {0:02X}'.format(a[ia], ia - la))
            listDels.append(ia)
            del B[ia-la]
            la += 1

        ia, ib = ia + da, ib + db


    hexa = map(lambda x: '{0:02X}'.format(x), a)
    hexb = map(lambda x: '{0:02X}'.format(x), b)


    print('='*20)

    print('Original:')
    print('='*47)
    print(tableize(colorize(hexa, {31: listDels, 33: listSubsa})))
    print('='*47)

    print('\n')

    print('Target:')
    print('='*47)
    print(tableize(colorize(hexb, {32: listIns, 33: listSubsa})))
    print('='*47)


    if b == B:
        print('OK')
    else:
        print('fail')

    return d[-1][-1]


#
# _____________________________________________________________________________
#
def getOptimalPath(d):

    path = []

    ia = len(d) - 1
    ib = len(d[0]) - 1
    while ia != 0 or ib != 0:
        if ia == 0:
            da, db = 0, 1
        elif ib == 0:
            da, db = 1, 0
        else:
            opDel = (d[ia-1][ib], 1, 0)
            opIns = (d[ia][ib-1], 0, 1)
            opSub = (d[ia-1][ib-1], 1, 1)
            opMin = min([opSub, opDel, opIns], key=lambda x: x[0])
            da, db = opMin[1], opMin[2]
        ia, ib = ia - da, ib - db
        path.insert(0, (da, db))

    return path


#
# _____________________________________________________________________________
#
def getMatrix(a, b):

    na = len(a)
    nb = len(b)

    # Prepare the (Levenshtein) distance matrix d[-a-][-b-]
    d = [[0 for i in range(nb + 1)] for j in range(na + 1)]
    for i in range(na + 1)[1:]:
        d[i][0] = i
    for j in range(nb + 1)[1:]:
        d[0][j] = j

    # Fill the (Levenshtein) distance matrix
    for j in range(nb + 1)[1:]:
        for i in range(na + 1)[1:]:
            opDel = d[i-1][j] + 1
            opIns = d[i][j-1] + 1
            opSub = d[i-1][j-1] + (0 if a[i-1] == b[j-1] else 1)
            d[i][j] = min(opSub, opDel, opIns)

    # Return the (Levenshtein) distance matrix
    return d


#
# _____________________________________________________________________________
#
def printMatrix(matrix, mr=None, mc=None):

    for ir, row in enumerate(matrix):
        line = ''
        for ic, cell in enumerate(row):
            if ir == mr and ic == mc:
                f = '~'
            else:
                f = ''
            line += '{0:^5}'.format('{1}{0}{1}'.format(cell, f))
        print(line)    


#
# _____________________________________________________________________________
#
if __name__ == "__main__":
    main(sys.argv[1:])




