#!/usr/bin/env python3
'''
Author: Maya Bose
Date: 5/17/2019
This program converts a fastq file to a fasta file.
'''
import sys
import gzip

def main():

    fn = sys.argv[1]

    i = 0
    with gzip.open(fn, 'r') as the_file:
        for line in the_file:
            line = line.decode('utf-8')
            line = line.strip()

            if i == 0:
                line = '>' + line[1:]

            line = line + "\n"
            line = line.encode('utf-8')

            if i == 0 or i == 1:
                sys.stdout.buffer.write(line)

            i += 1
            if i == 4:
                i = 0


main()
