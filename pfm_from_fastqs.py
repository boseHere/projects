#!/usr/bin/env python3
"""
This program takes in fastq files and outputs a comma-separated values file 
containing a Position Frequency Matrix (PFM) for reads of a given length.
"""
__author__ = "boseHere"
import argparse
import gzip

def get_args():
    """
    This function uses the argparse library to parse command line arguments.
    :param: none
    :return: args -- An argparse object. Elements of the object can be accessed
                     by their option name as attributes)
    """
    parser = argparse.ArgumentParser(description="This program takes in fastq \
        files and outputs a comma-separated values file containing the count \
            of each nucleotide base at each position in reads of a given \
                length.")
    parser.add_argument("input", type=str, nargs="+", 
                    help="Input fastq files. Input can be gzipped files")
    parser.add_argument("seq_length", type=int, help="Length of reads")
    parser.add_argument("--progress", action="store_true", 
                    help="Print when a file has completed \
                    processing to the terminal. Helpful to use if inputting \
                    many files")
    parser.add_argument("--output_dir", type=str, nargs="?", const="./",
    default="./", help="Set output diretory for pfm text file. Default is \
        current directory")

    args = parser.parse_args()

    return args

def make_pfm(args):
    """
    This function iterates through the given files to create a list of lists
    containing the nucleotide base count at each position.
    :param: args -- An argparse object. Elements of the object can be accessed
                     by their option name as attributes)
    :return: pfm -- A list of lists containing a Position Frequency Matrix.
    """
    pfm = [[0] * 4 for _ in range(args.seq_length)]
    for file in args.input:
        if file.endswith(".gz"):
            ofile = gzip.open(file, "r")
        else:
            ofile = open(file, "r")
        i = 0
        for line in ofile:
            if file.endswith(".gz"):
                line = line.decode("utf-8")
            line = line.strip()
            if i == 1 and len(line) == args.seq_length:
                for j in range(len(line)):
                    if line[j] == "A":
                        pfm[j][0] += 1
                    elif line[j] == "C":
                        pfm[j][1] += 1
                    elif line[j] == "G":
                        pfm[j][2] += 1
                    elif line[j] == "T":
                        pfm[j][3] += 1
            i += 1
            if i == 4:
                 i = 0

        if args.progress:
            print("{} finished processing".format(file)
    
    return pfm

def write_pfm(args, pfm):
    """
    This function writes the PFM to a comma-sepearated text output file. 
    """
    with open(args.output_dir + str(args.seq_length) + "_pfm.txt", "w+") as fo:
        fo.write("Position, A, C, G, T")
        for i in range(len(pfm)):
            for j in range(len(pfm[i])):
                pfm[i][j] = str(pfm[i][j])
        i = 0
        for row in pfm:
            fo.write(str(i) + ", " + ", ".join(row) + "\n")
            i += 1

def main():
    args = get_args()
    pfm = make_pfm(args)
    write_pfm(args, pfm)
    

if __name__ == "__main__":
    main()
