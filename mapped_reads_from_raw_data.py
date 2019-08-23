#!/usr/bin/python3
"""
Author: Maya Bose
Date: 7/30/19
Purpose: Given a fastq file of reads that mapped to a reference genome and a
fastq file of raw reads, this program retrieves the reads from the file of raw
data that are present in the file of mapped reads.
"""
__author__ = "boseHere"
import argparse
import gzip
import os

def get_args():
    """
    This function uses the argparse library to parse command line arguments.
    :param: none
    :return: args -- An argparse object. Elements of the object can be accessed
                     by their option name as attributes (e.g. args.gzip returns
                     the user input for the gzip option)
    """
    parser = argparse.ArgumentParser(description="This script filters reads"
                                                 "within a given range of "
                                                 "lengths, to be used on fastq"
                                                 "files that have already been"
                                                 "adapter-trimmed")
    parser.add_argument("input_raw", type=str,
                        help="Fastq filename with raw reads")
    parser.add_argument("input_mapped", type=str,
                        help="Fastq filename with reads that have mapped to "
                             "the genome")
    parser.add_argument("--gzip", help="Gzip the output file",
                        action="store_true")
    parser.add_argument("--output_dir", nargs="?", type=str, const="./",
                        default="./", help="Directory location for output file."
                                           " Set to current directory by "
                                           "default")
    args = parser.parse_args()
    return args

def create_params(args):
    """
    This function uses attributes of the args object to create parameters for
    the filter function. This function also tests to ensure valid user inputs
    for minimum and maximum length.
    :param: args: -- An argparse object. Elements of the object can be accessed
                     by their option name as attributes (e.g. args.gzip returns
                     the user input for the gzip option)
    :returns: gzipped -- A boolean. True if the input file is in gzipped format.
                         Not to be confused with args.gzip, which is True if
                         the output file is to be gzipped.

              outfile -- The name of the file where output is to be written to.
                         Consists of {output directory} + "trimmed_" + {length
                         range}_ + {input file name}
    """

    # Initialize the name of the output file to the name of the input file
    path = os.path.abspath(args.input_raw)
    base = path.rfind("/")
    if base == -1:
        outfile = args.input_raw
    else:
        outfile = path[base + 1:]

    outfile = "filtered_" + outfile

    # Add output directory path to output file name
    outfile = str(args.output_dir) + outfile

    # If the input file is in gzipped format, remove the gzip file extension
    # from the output file name and set the value of the variable gzipped to
    # true.
    if args.input_raw[-3:] == ".gz":
        gzipped1 = True
        outfile = outfile[:-3]
    else:
        gzipped1 = False

    gzipped2 = (args.input_mapped[-3:] == ".gz")

    # If the --gzip option has been used, add the gzip file extension to the
    # output file name
    if args.gzip:
        outfile = outfile + ".gz"

    return gzipped1, gzipped2, outfile


def open_files(args, outfile, gzipped1, gzipped2):
    """
    This function opens the input file for reading and opens the output file
    for writing.
    :params: args -- An argparse object. Elements of the object can be accessed
                     by their option name as attributes (e.g. args.gzip returns
                     the user input for the gzip option)

             outfile -- The name of the file to be written to.
    :returns: infile -- A file object to be read from.

              writefile -- A file object to be written to.
    """
    try:
        if args.gzip:
            writefile = gzip.open(outfile, "w+")
        else:
            writefile = open(outfile, "w+")
    except FileNotFoundError:
        print("Output directory does not exist")
        exit(1)

    try:
        if gzipped1:
            infile1 = gzip.open(args.input_raw, "r")
        else:
            infile1 = open(args.input_raw, "r")
    except FileNotFoundError:
        print("Raw data input file does not exist")
        exit(1)

    try:
        if gzipped2:
            infile2 = gzip.open(args.input_mapped, "r")
        else:
            infile2 = open(args.input_mapped, "r")
    except FileNotFoundError:
        print("Mapped data input file does not exist")
        exit(1)

    return infile1, infile2, writefile


def raw_reads_dictionary(infile1, gzipped1):
    i = 0
    reads = {}
    for line in infile1:
        if gzipped1:
            line = line.decode("utf-8")
        line = line.strip()
        if i == 0:
            line1 = line.split()
            line1 = line1[0]
            reads[line1] = []
        elif i == 1 or i == 2 or i == 3:
            reads[line1].append(line)
        i += 1
        if i == 4:
            i = 0
    return reads


def intersect_reads(args, reads, infile2, gzipped2, writefile):
    i = 0
    for line in infile2:
        if gzipped2:
            line = line.decode("utf-8")
        line = line.strip()
        if i == 0:
            line1 = line + "\n"
            line2 = reads[line][0] + "\n"
            line3 = reads[line][1] + "\n"
            line4 = reads[line][2] + "\n"

            if args.gzip:
                line1 = line1.encode("utf-8")
                line2 = line2.encode("utf-8")
                line3 = line3.encode("utf-8")
                line4 = line4.encode("utf-8")

            writefile.write(line1)
            writefile.write(line2)
            writefile.write(line3)
            writefile.write(line4)

        i += 1
        if i == 4:
            i = 0


if __name__ == "__main__":
    args = get_args()
    gzipped1, gzipped2, outfile = create_params(args)
    infile1, infile2, writefile = open_files(args, outfile, gzipped1, gzipped2)
    reads = raw_reads_dictionary(infile1, gzipped1)
    intersect_reads(args, reads, infile2, gzipped2, writefile)

    infile1.close()
    infile2.close()
    writefile.close()
