# Load ROOT modules
from ROOT import TH1D, gROOT, gSystem

# Import TTree branching module
from inspectData import readMC, addToChain
from stuff import createOutROOTFile


def analyzeMC(opts):

    # Load DAMPE libs
    gSystem.Load("libDmpEvent.so")
    gSystem.Load("libDmpKernel.so")
    gSystem.Load("libDmpService.so")

    # Load DAMPE modules
    from ROOT import DmpChain

    # Set ROOT verbosity
    gROOT.SetBatch(True)
    gROOT.ProcessLine("gErrorIgnoreLevel = %i;" % opts.verbose)

    # Create output TFile
    outFile = createOutROOTFile(opts)

    # Create eKin energy histo
    nBins = 10000
    xLow = 0
    xUp = 200000
    eKinHisto = TH1D("eKinHisto", "MC Trye Kinetic Energy", nBins, xLow, xUp)

    # Creating DAMPE chain for input files
    dmpch = DmpChain("CollectionTree")

    # Add ROOT files to the chain and get total events
    nevents = addToChain(opts, dmpch)

    # Analyze events
    readMC(opts, dmpch, nevents, eKinHisto, kStep=1e+4)

    # Write histo to TFile
    eKinHisto.Write()

    # Write output TFile
    outFile.Write()
