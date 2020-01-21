#!/usr/bin/env python

import sys
from datetime import datetime
from argparse import ArgumentParser

start=datetime.now()

def main(args=None):
    ### Parsing options
    parser = ArgumentParser(usage="Usage: %(prog)s [options]", description="nTuple to TTree converter")
    
    parser.add_argument("-i","--input", type=str, dest='input', help='ROOT MC ROOT files directory')
    parser.add_argument("-o","--output", type=str, dest='output', default="MCheck.root" , help='name of output root TFile')
    parser.add_argument("-v","--verbose", dest='verbose', default=False, action='store_true', help='run in high verbosity mode')
    parser.add_argument("-d","--debug", type=int, dest='debug', const=1000, nargs='?', help='activate debug mode - const value 1000 events')

    opts = parser.parse_args(args)

    #Load analysis functions
    sys.path.append("moduls")
    from kompressor import analyzeMC

    analyzeMC(opts)

if __name__ == '__main__':
    main()
    print datetime.now()-start