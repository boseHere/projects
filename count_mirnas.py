#!/usr/bin/env python3

'''
Author: Maya Bose
Date: 5/18/19
Counts occurrences of matches between sequences in miRNA fasta file and  srna
fastq file.
'''
import argparse
import gzip


def main():
    d = get_args()
    mirna_dict = make_mirna_dict(d)
    mirna_dict = count(mirna_dict, d)
    output(mirna_dict)


def get_args():
    parser = argparse.ArgumentParser(description="Take sRNA seq run; identifies"
                                                 "counts of those sequences in"
                                                 "a given miRNA reference "
                                                 "genome")
    parser.add_argument('sRNA file', metavar='n', type=str, nargs=1,
                        help='The sRNA seq filename')
    parser.add_argument('miRNA file', metavar='s', type=str, nargs=1, help='The\
    miRNA reference filename')
    args = parser.parse_args()
    d = vars(args)
    return d


def make_mirna_dict(d):
    mirna_dict = {}
    with gzip.open(d['miRNA file'][0], 'r') as rfile:
        for line in rfile:
            line = line.decode('utf-8')
            if line.startswith(">"):
                ref = line.rstrip('\n')
            else:
                seq = line.rstrip('\n')
                mirna_dict[seq] = [ref, 0]

    return mirna_dict


def count(mirna_dict, d):
    with gzip.open(d['sRNA file'][0], 'r') as sfile:
        i = 0
        for line in sfile:
            line = line.decode('utf-8')
            line = line.rstrip('\n')
            if i == 1:
                seq = line.replace('T', 'U')
                if seq in mirna_dict:
                    mirna_dict[seq][1] += 1
            i += 1
            if i == 5:
                i = 0
    return mirna_dict


def output(mirna_dict):
    for seq in mirna_dict:
        print("{}\n{}\nCount:{}".format(seq, mirna_dict[seq][0],
                                        mirna_dict[seq][1]))


main()
