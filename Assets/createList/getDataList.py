# /usr/bin/env python3
import sys
from argparse import ArgumentParser


def main(args=None):
    # Parsing options
    parser = ArgumentParser(
        usage="Usage: %(prog)s [options]", description="Create a list of files from an input dir")

    parser.add_argument("-i", "--input", type=str,
                        dest='input', help='Input data directory')
    parser.add_argument("-o", "--output", type=str,
                        dest='output', help='Output file list')
    parser.add_argument("-n", "--number", type=int, dest='fileNumber',
                        const=100, nargs='?', help='number of files to include')
    parser.add_argument("-v", "--verbose", dest='verbose', default=False,
                        action='store_true', help='run in high verbosity mode')

    opts = parser.parse_args(args)

    sys.path.append("../condorHelper/moduls")
    from dirParser import parseInputDir

    # Loop over the list
    if opts.output:
        parseInputDir(opts, noSplitList=True, singleListOutput=opts.output)
    else:
        parseInputDir(opts, noSplitList=True)

if __name__ == '__main__':
    main()
