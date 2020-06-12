#!/usr/bin/env python
from argparse import ArgumentParser
from ROOT import TFile, TH1D, gSystem
import os

def createOutFile(opts):
    outFilePath = opts.directory + "/MCheck_outFile.root"
    try:
        outFile = TFile(outFilePath, "RECREATE")
    except OSError:
        print('Error writing output file {}'.format(outFilePath))
        raise
    else:
        if opts.verbose:
            print('Default output ROOT file has been created: {}'.format(outFilePath))
        else:
            if opts.verbose:
                print('Output ROOT file has been created: {}'.format(outFilePath))
    return outFile 

def addToChain(opts, mcChain):

    # Load DAMPE libs
    gSystem.Load("libDmpEvent.so")
    gSystem.Load("libDmpKernel.so")
    gSystem.Load("libDmpService.so")

    from ROOT import DmpChain
    from ROOT import DmpVSvc

    # Load DAMPE modules
    import DMPSW
    
    if opts.verbose:
        print('Reading input ROOT files from list: {}'.format(opts.list))
    files = [f.replace("\n", "") for f in open(opts.list, 'r').readlines()]
    for idxFile, f in enumerate(files):
        DMPSW.IOSvc.Set("InData/Read" if idxFile == 0 else "InData/ReadMore", f)
        mcChain.Add(f)
           
    nevents = mcChain.GetEntries()
    if opts.verbose:
        print('Collected {} events ...'.format(nevents))

    return nevents

def readMC(opts, mcChain, nevents, eKinHisto, kStep):

    # Load DAMPE libs
    gSystem.Load("libDmpEvent.so")
    gSystem.Load("libDmpKernel.so")
    gSystem.Load("libDmpService.so")

    from ROOT import DmpChain
    from ROOT import DmpVSvc

    if opts.verbose:
        print("Reading TChain data ...")

    for idx in range(nevents):
        DmpVSvc.gPsdECor.SetMCflag(1)
        pev = mcChain.GetDmpEvent(idx)
        eKinHisto.Fill(pev.pEvtSimuPrimaries().pvpart_ekin)
        eventProcess(opts, idx, nevents, kStep)
            

def eventProcess(opts, evIdx, totEvents, kStep=1):
    if opts.verbose:
        if (evIdx % kStep) == 0 and evIdx != 0:
            print('\tProcessed event {} of {}'.format(evIdx, totEvents))

def main(args=None):
    # Parsing options
    parser = ArgumentParser(
        usage="Usage: %(prog)s [options]", description="MonteCarlo Analyzer")

    parser.add_argument("-l", "--list", type=str,
                        dest='list', help='Input file list')
    parser.add_argument("-d", "--dir", type=str,
                        dest='directory', help='Target Directory')
    parser.add_argument("-v", "--verbose", dest='verbose', default=False,
                        action='store_true', help='run in high verbosity mode')

    opts = parser.parse_args(args)
    
    # Create eKin energy histo
    nBins = 10000
    xLow = 0
    xUp = 200000
    eKinHisto = TH1D("eKinHisto", "MC True Kinetic Energy", nBins, xLow, xUp)

    # Load DAMPE libs
    gSystem.Load("libDmpEvent.so")
    gSystem.Load("libDmpKernel.so")
    gSystem.Load("libDmpService.so")

    from ROOT import DmpChain
    from ROOT import DmpVSvc

    # Load DAMPE modules
    import DMPSW

    # Creating DAMPE chain for input files
    dmpch = DmpChain("CollectionTree")

    # Add ROOT files to the chain and get total events
    nevents = addToChain(opts, dmpch)

    # Analyze events
    readMC(opts, dmpch, nevents, eKinHisto, kStep=1e+4)
    
    # Create output ROOT TFile
    outFile = createOutFile(opts)
   
    # Write histo to TFile
    eKinHisto.Write()
    
    # Write output TFile
    outFile.Write()

if __name__ == '__main__':
    main()
