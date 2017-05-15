#!/usr/bin/python

import sys

class tf(object):

    useColor = True

    strColorEnd = '\033[0m'

    @staticmethod
    def makeBoldWhite(s):
        if tf.useColor:
            return '\033[1m' + s + tf.strColorEnd
        return s

    @staticmethod
    def makeBoldRed(s):
        if tf.useColor:
            return '\033[1;31m' + s + tf.strColorEnd
        return s

    @staticmethod
    def makeBoldGreen(s):
        if tf.useColor:
            return '\033[1;32m' + s + tf.strColorEnd
        return s

    @staticmethod
    def makeBoldYellow(s):
        if tf.useColor:
            return '\033[1;33m' + s + tf.strColorEnd
        return s

    @staticmethod
    def makeBoldBlue(s):
        if tf.useColor:
            return '\033[1;34m' + s + tf.strColorEnd
        return s

    @staticmethod
    def makeBoldPurple(s):
        if tf.useColor:
            return '\033[1;35m' + s + tf.strColorEnd
        return s

    @staticmethod
    def makeBoldCyan(s):
        if tf.useColor:
            return '\033[1;36m' + s + tf.strColorEnd
        return s

    @staticmethod
    def makeGreen(s):
        if tf.useColor:
            return '\033[32m' + s + tf.strColorEnd
        return s

    @staticmethod
    def makeRed(s):
        if tf.useColor:
            return '\033[31m' + s + tf.strColorEnd
        return s

    @staticmethod
    def makeBlue(s):
        if tf.useColor:
            return '\033[34m' + s + tf.strColorEnd
        return s

    @staticmethod
    def indent(str, level=1):
        lines = [' '*(4 if s else 0)*level + s for s in str.split('\n')]
        return '\n'.join(lines)


#
# _____________________________________________________________________________
#
def usage():
    print('Usage: ./parse_gcov.py COMMAND [OPTIONS] FILE1 [FILE2]')
    exit(0)


#
# _____________________________________________________________________________
#
def main(argv):

    if len(argv) < 1:
        usage()

    cmd = argv[0]

    argFileIndex = None
    for i, arg in enumerate(argv):
        if i == 0:
            # Skip command
            continue
        if not arg.startswith('-'):
            argFileIndex = i
            break   

    if argFileIndex is None:
        print('Missing input file')
        usage()

    args = argv[1:argFileIndex]
    files = argv[argFileIndex:]

    flags = '-s' in args

    if cmd == 'print':
        do_print(files)
    elif cmd == 'diff':
        if len(files) != 2:
            print('Invalid number of input files for "diff"')
            usage()
        else:
            do_diff(files[0], files[1])
    elif cmd == 'extract':
        do_extract(files, flags)
    else:
        print('Unknown command "{0}"'.format(cmd))
        usage()


#
# _____________________________________________________________________________
#
def do_print(files):

    for filename in files:

        print(tf.makeBoldWhite('Printing file "{0}":'.format(filename)))

        lines_exec, lines_code = read_gcov_file(filename)

        for i in range(len(lines_code)):
            n = lines_exec[i + 1] 
            if n == 0:
                lines_code[i] = tf.makeBoldRed(lines_code[i])            
            elif n is not None and n > 0:
                lines_code[i] = tf.makeBoldGreen(lines_code[i])            
     
        print(''.join(lines_code))


#
# _____________________________________________________________________________
#
def do_extract(files, skip_nonexecutable=False):

    extracted = []

    for filename in files:

        lines_exec, lines_code = read_gcov_file(filename, read_code=False)

        for i in range(len(lines_exec)):
            n = lines_exec[i + 1] 
            if n is None:
                if not skip_nonexecutable:
                    extracted.append('-') 
            elif n == 0:
                extracted.append('0') 
            else:
                extracted.append('1') 

    print(''.join(extracted))


#
# _____________________________________________________________________________
#
def do_diff(file1, file2):

    lines_exec_1, lines_code_1 = read_gcov_file(file1)
    lines_exec_2, lines_code_2 = read_gcov_file(file2)

    if ''.join(lines_code_1) != ''.join(lines_code_2):
        print('Cannot "diff": mismatching source code')
        exit(1)

    print_out = []

    w = len(str(len(lines_code_1) + 1))

    for i in range(len(lines_code_1)):
        n1 = lines_exec_1[i + 1] 
        n2 = lines_exec_2[i + 1]
        code = lines_code_1[i]

        line_head = ' {0:{1}} '.format(i + 1, w)
        line_exec = ''

        if (n1 is None) != (n2 is None):
            print('WARNING: mismatch in line executability')
            exit(1)
        elif (n1 > 0) != (n2 > 0):
            if n1 > 0:
                code_line = tf.makeBoldPurple(code)            
                line_head = tf.makeBoldPurple(line_head)
                line_exec = tf.makeBoldPurple('[X] [-]')
            else:
                code_line = tf.makeBoldCyan(code)            
                line_head = tf.makeBoldCyan(line_head)            
                line_exec = tf.makeBoldCyan('[-] [X]')
        else:
            if n1 == 0:
                code_line = tf.makeBoldRed(code)          
                line_head = tf.makeBoldRed(line_head)            
                line_exec = tf.makeBoldRed('[-] [-]')
            elif n1 is not None:
                code_line = tf.makeBoldGreen(code)             
                line_head = tf.makeBoldGreen(line_head)            
                line_exec = tf.makeBoldGreen('[X] [X]')
            else:
                code_line = code
                line_exec = '       '

        print_out.append('{0}| {1} | {2}'.format(line_head, line_exec, code_line))

    print(''.join(print_out))



#
# _____________________________________________________________________________
#
def read_gcov_file(filename, **options):

    read_code = options.get('read_code', True)

    f = open(filename)
    if f:
        #print('Reading gcov file "{0}" ...'.format(filename))
        lines_exec, lines_code = parse_gcov(f, **options)

        if read_code and (len(lines_exec) != len(lines_code)):
            print('WARNING: mismatch of line numbers!')

    else:
        print('Failed to read gcov file "{0}" ...'.format(filename))
        lines_exec = None
        lines_code = None

    return lines_exec, lines_code


#
# _____________________________________________________________________________
#
def parse_gcov(text, **options):

    read_code = options.get('read_code', True)

    lines_exec = {}
    lines_code = []

    for line in text:
        tokens = line.split(':')
        if '#' in tokens[0]:
            n_exec = 0
        else:
            try:
                n_exec = int(tokens[0])
            except ValueError:
                n_exec = None
        i_line = int(tokens[1])
        if read_code:
            code = ':'.join(tokens[2:])

        if i_line > 0:
            lines_exec[i_line] = n_exec
            if read_code:
                if (len(lines_code) + 1) != i_line:
                    print('WARNING: invalid line order in source code')
                lines_code.append(code)

    return lines_exec, lines_code

#
# _____________________________________________________________________________
#
if __name__ == "__main__":
    main(sys.argv[1:])

