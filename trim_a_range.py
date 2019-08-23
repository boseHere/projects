#!/usr/bin/python3

"""
Author: Maya Bose
Last updated: 7/26/19
This program filters reads by length from a fastq file (.fastq, .fq, .fastq.gz,
.fq.gz) into a fastq file. Options include a minimum length and maximum length
to filter by, an output directory, and the option to gzip the output file.
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
                                                 "lengths, to be used on fastq "
                                                 "files that have already been "
                                                 "adapter-trimmed")
    parser.add_argument("input", type=str, help="Input file name")
    parser.add_argument("--gzip", help="Gzip the output file",
                        action="store_true")
    parser.add_argument("--min_length", nargs='?', type=int, const=0, default=0,
                        help="Shortest read length to include in output. Set "
                             "to 0 by default")
    parser.add_argument("--max_length", type=int,
                        help="Longest read length to include in output",
                        required=False)
    parser.add_argument("--output_dir", nargs='?', type=str, const="./",
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
                         Consists of {output directory} + 'trimmed_' + {length
                         range}_ + {input file name}
    """

    # Initialize the name of the output file to the name of the input file
    path = os.path.abspath(args.input)
    base = path.rfind("/")
    if base == -1:
        outfile = args.input
    else:
        outfile = path[base + 1:]

    # Test for valid user input for minimum and maximum read lengths.
    if args.min_length < 0:
        print("Minimum read length must be greater than or equal to 0")
        exit(1)

    if args.max_length:
        if args.max_length < 0:
            print("Maximum read length must be greater than or equal to 0")
            exit(1)

        if args.max_length < args.min_length:
            print("Minimum read length must be less than or equal to "
                  "maximum read length")
            exit(1)

        # Add read length range to name of output file
        outfile = "trimmed_" + str(args.min_length) + "_" + \
                  str(args.max_length) + "_" + outfile
    else:
        # Add read length range to name of output file (if no max length is
        # given)
        outfile = "trimmed_" + str(args.min_length) + "_maxLen_" + outfile

    # Add output directory path to output file name
    outfile = str(args.output_dir) + outfile

    # If the input file is in gzipped format, remove the gzip file extension
    # from the output file name and set the value of the variable gzipped to
    # true.
    if args.input[-3:] == ".gz":
        gzipped = True
        outfile = outfile[:-3]
    else:
        gzipped = False

    # If the --gzip option has been used, add the gzip file extension to the
    # output file name
    if args.gzip:
        outfile = outfile + ".gz"

    return gzipped, outfile


def open_files(args, outfile):
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
        if gzipped:
            infile = gzip.open(args.input, "r")
        else:
            infile = open(args.input, "r")
    except FileNotFoundError:
        print("Input file does not exist")
        exit(1)

    return infile, writefile


def filter(args, gzipped, infile, writefile):
    """
    This function loops through the input file, determines which reads fit
    within the given length range, and write these reads and their information
    to the output file.
    :params: args -- An argparse object. Elements of the object can be accessed
                     by their option name as attributes (e.g. args.gzip returns
                     the user input for the gzip option)

             gzipped -- A boolean. True if the input file is in gzipped format.
                         Not to be confused with args.gzip, which is True if
                         the output file is to be gzipped.

             infile -- A file object to be read from.

             writefile -- A file object to be written to.
    :return: none
    """

    i = 0
    fits = False

    for line in infile:
        if gzipped:
            line = line.decode("utf-8")
        line = line.strip()

        if i == 0:
            line1 = line + "\n"

        # Second line of every read entry (total 4 lines) in fastq format is
        # actual read sequence. Test if the length of this read is within the
        # user given range of lengths.
        elif i == 1:

            if args.max_length:
                if args.min_length <= len(line) <= args.max_length:
                    fits = True
                else:
                    fits = False
            else:
                if args.min_length <= len(line):
                    fits = True
                else:
                    fits = False
            line2 = line + "\n"
        elif i == 2:
            line3 = line + "\n"

        elif i == 3 and fits:  # If the length of the read sequence from line 2
                                # was within  the user given range of lengths,
                                # write all the information for that read to the
                                # output file.
            line4 = line + "\n"

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
    gzipped, outfile = create_params(args)
    infile, writefile = open_files(args, outfile)
    filter(args, gzipped, infile, writefile)

    writefile.close()
    infile.close()
