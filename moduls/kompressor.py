import sys

### Load ROOT modules
from ROOT import TClonesArray, TFile, TTree, gSystem, gROOT, AddressOf
from ROOT import TH1D, TMath, TGraphAsymmErrors

# Import TTree branching module
from inspectData import readMC,addToChain

def analyzeMC(opts):
    
    ###Load DAMPE libs

    gSystem.Load("libDmpEvent.so")
    gSystem.Load("libDmpEventFilter.so")
    
    gSystem.Load("libDmpKernel.so")
    gSystem.Load("libDmpService.so")

    ###Load DAMPE modules

    from ROOT import DmpChain, DmpEvent, DmpFilterOrbit, DmpPsdBase, DmpCore
    from ROOT import DmpSvcPsdEposCor, DmpVSvc   #DmpRecPsdManager
    import DMPSW

    gROOT.SetBatch(True)

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
    
    ####### Reading input files

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

    