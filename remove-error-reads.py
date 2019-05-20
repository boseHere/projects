#!/usr/bin/env python3
'''
Author: Maya Bose
Date: 5/20/19
This program removes the last base of error-prone full-length reads from a
fastq file.
'''


import argparse
import gzip


def main():
    d = get_args()
    strip_error_bases(d)


def get_args():
    parser = argparse.ArgumentParser(description="Removes the last base of"
                                                 "error-prone full-length"
                                                 "(Target length) reads "
                                                 "from a fastq file")
    parser.add_argument('RNA file', metavar='n', type=str, nargs=1,
                        help='The RNA seq filename')
    parser.add_argument('Target length', metavar='l', type=int, nargs=1, help=
                        'Target length of a read')
    args = parser.parse_args()
    d = vars(args)
    return d


def strip_error_bases(d):
    with gzip.open(d['RNA file'][0], 'r') as rfile:
        i = 0
        for line in rfile:
            line = line.decode('utf-8')
            line = line.rstrip('\n')
            if i == 1 or i == 3:

                # Reduce over-read lines to target length
                if len(line) > d['Target length'][0]:
                    trim = len(line) - d['Target length'][0]
                    line = line[:-1 * trim]
                    
            print(line)
            i += 1
            if i == 4:
                i = 0


main()
