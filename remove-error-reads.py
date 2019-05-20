#!/usr/bin/env python3

import argparse
import gzip


def main():
    d = get_args()


def get_args():
    parser = argparse.ArgumentParser(description="Take sRNA seq run; identifies"
                                                 "counts of those sequences in"
                                                 "a given miRNA reference "
                                                 "genome")
    parser.add_argument('RNA file', metavar='n', type=str, nargs=1,
                        help='The RNA seq filename')
    args = parser.parse_args()
    d = vars(args)
    return d


def strip_error_bases(d):
    with gzip.open(d['RNA file']) as rfile:
        for line in rfile:
            line = line.decode('utf-8')
            line = line.rstrip('\n')
            if len(line) > 73:

main()