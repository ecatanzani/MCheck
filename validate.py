#!/usr/bin/env python
import os
import sys
from datetime import datetime
from argparse import ArgumentParser

start=datetime.now()

def main(args=None):
    ### Parsing options
    parser = ArgumentParser(usage="Usage: %(prog)s [options]", description="MonteCarlo Analyzer")
    
    parser.add_argument("-i","--input", type=str, dest='input', help='MC ROOT input directory')
    parser.add_argument("-l","--list", type=str, dest='list', help='MC ROOT input file list')
    #arser.add_argument("-o","--output", type=str, dest='output', default="MCheck.root" , help='name of output root TFile')
    parser.add_argument("-o","--output", type=str, dest='output', help='name of output root TFile')
    parser.add_argument("-v","--verbose", dest='verbose', default=False, action='store_true', help='run in high verbosity mode')
    parser.add_argument("-d","--debug", type=int, dest='debug', const=1000, nargs='?', help='activate debug mode - const value 1000 events')
    parser.add_argument("-w","--wdir", type=str, dest='workingDir', help='Home WD - HTCondor system')

    opts = parser.parse_args(args)

    #Load analysis functions
    if not opts.workingDir:
        sys.path.append("moduls")
    else:
        modAbsPath = opts.workingDir + "/moduls"
        sys.path.append(modAbsPath)
    from kompressor import analyzeMC
    from stuff import createOutDir
    
    # Start analysis routine
    analyzeMC(opts)

if __name__ == '__main__':
    main()
    print datetime.now()-start