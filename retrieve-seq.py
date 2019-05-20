#!/usr/bin/env python3
'''
Author: Maya Bose
Date: 5/17/19
This program takes the name of a chromosome, the index of the start base, and
the index of the end base, and outputs the bases within the given base range.
'''

import argparse
import gzip


def main():

    parser = argparse.ArgumentParser(description="Retrieve sequences from a "
                                                 "reference genome given "
                                                 "coordinates")
    parser.add_argument('Chromosome name', metavar='n', type=str, nargs=1,
                        help='The name of the chromosome/scaffold where the'
                             'sequence is')
    parser.add_argument('Start', metavar='s', type=int, nargs=1, help='The\
number of the base where the sequence starts.')
    parser.add_argument('End', metavar='e', type=int, nargs=1, help='The\
    number of the base where the sequence starts.')
    args = parser.parse_args()
    d = vars(args)

    with gzip.open('genome.fa.gz', 'rt') as the_file:
        k = False
        output = ""
        for line in the_file:
            line = line.strip()
            line = line.decode('utf-8')
            seq_line_length = len(line)
            if line[1:] == d['Chromosome name']:
                k = 0

            elif k != False:
                if d['Start'][0] <= k <= d['End'][0]:
                    if k >= seq_line_length:
                        index = k % seq_line_length
                    else:
                        index = k

                    output += str(line[index])
                if k == d['End'][0]:
                    break
            k += 1

        print(output)


main()
