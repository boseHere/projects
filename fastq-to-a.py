#!/usr/bin/env python3
'''
Author: Maya Bose
Date: 5/17/2019
This program converts a fastq file to a fasta file.
'''
import gzip
import argparse


def main():

    d = get_args()
    convert(d)


def get_args():
    parser = argparse.ArgumentParser(
        description="Converts a fastq file to fasta format")
    parser.add_argument('Filename', metavar='f', type=str, nargs=1,
                        help='a fastq file')
    args = parser.parse_args()
    d = vars(args)

    return d

def convert(d):
    i = 0
    with gzip.open(d['Filename'][0], 'r') as the_file:
        for line in the_file:
            line = line.decode('utf-8')
            line = line.strip()

            if i == 0:
                line = '>' + line[1:]

            line = line + "\n"
            line = line.encode('utf-8')

            if i == 0 or i == 1:
                print(line)

            i += 1
            if i == 4:
                i = 0


main()
