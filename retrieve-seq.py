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
    d = get_args()
    chr = retrieve_scaffold(d)
    find_seq(chr, d)


def get_args():
    parser = argparse.ArgumentParser(description="Retrieve sequences from a "
                                                 "reference genome given "
                                                 "coordinates")
    parser.add_argument('Filename', metavar='f', type=str, nargs=1,
                        help='a fasta file')
    parser.add_argument('Chromosome name', metavar='n', type=str, nargs=1,
                        help='The name of the chromosome/scaffold where the'
                             'sequence is')
    parser.add_argument('Start', metavar='s', type=int, nargs=1, help='The\
number of the base where the sequence starts.')
    parser.add_argument('End', metavar='e', type=int, nargs=1, help='The\
    number of the base where the sequence starts.')
    args = parser.parse_args()
    d = vars(args)

    return d


def retrieve_scaffold(d):
    with gzip.open(d['Filename'][0]) as the_file:
        k = False
        data = []
        for line in the_file:
            line = line.strip()
            line = line.decode('utf-8')

            if line[1:] == d['Chromosome name'][0]:
                k = True

            elif k:
                if line.startswith(">"):
                    break
                else:
                    data.append(line)

        return data


def find_seq(chr, d):
    full_chr = "".join(chr)
    for i in range(d['Start'][0], d['End'][0] + 1):
        print(full_chr[i], end="")
    print()


main()
