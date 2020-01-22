#!/usr/bin/env python3
import sys
from argparse import ArgumentParser


def main(args=None):
    # Parsing options
    parser = ArgumentParser(
        usage="Usage: %(prog)s [options]", description="Condor Deploy Helper")

    parser.add_argument("-i", "--input", type=str,
                        dest='input', help='MC ROOT input directory')
    parser.add_argument("-l", "--list", type=str,
                        dest='list', help='MC ROOT input file list')
    parser.add_argument("-n", "--number", type=int, dest='fileNumber',
                        const=100, nargs='?', help='number of files per job')
    parser.add_argument("-v", "--verbose", dest='verbose', default=False,
                        action='store_true', help='run in high verbosity mode')

    opts = parser.parse_args(args)

    # Load parsing functions
    sys.path.append("moduls")
    from dirParser import parseInputDir
    from listParser import parseInputList

    if opts.input:
        parseInputDir(opts)
    if opts.list:
        parseInputList(opts)


if __name__ == '__main__':
    main()
