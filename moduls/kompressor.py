import sys

### Load ROOT modules
from ROOT import TFile, TH1D,TTree,gROOT,gSystem

# Import TTree branching module
from inspectData import readMC,addToChain

def analyzeMC(opts):
    
    # Load DAMPE libs
    gSystem.Load("libDmpEvent.so")
    gSystem.Load("libDmpKernel.so")
    gSystem.Load("libDmpService.so")

    # Load DAMPE modules
    from ROOT import DmpChain

    # Set ROOT verbosity
    gROOT.SetBatch(True)
    gROOT.ProcessLine("gErrorIgnoreLevel = %i;"%opts.verbose)

    # Create output TFile
    outFile = TFile(opts.output,"RECREATE")
    if outFile.IsZombie():
        print('Error writing output file {}'.format(opts.output))
        sys.exit()
    
    # Create eKin energy histo
    nBins = 10000
    xLow = 0
    xUp = 200000
    eKinHisto = TH1D("eKinHisto","MC Trye Kinetic Energy",nBins,xLow,xUp)
    
    #Creating DAMPE chain for input files
    dmpch = DmpChain("CollectionTree")

    # Add ROOT files to the chain
    addToChain(opts,dmpch)

    nevents = dmpch.GetEntries()
    if opts.verbose:
        print('Collected {} events ...'.format(nevents))
    
    nevents = dmpch.GetEntries()
    readMC(opts,dmpch,nevents,eKinHisto,kStep=1e+4)

    # Write histo to TFile
    eKinHisto.Write()

    # Write output TFile
    outFile.Write()

    