import os
from tqdm import tqdm
from ROOT import TClonesArray, TFile, TTree, gSystem, gROOT, AddressOf
from ROOT import TH1D, TMath, TGraphAsymmErrors

from stuff import eventProcess

def addToChain(opts,mcChain):
    
    ###Load DAMPE libs

    gSystem.Load("libDmpEvent.so")
    gSystem.Load("libDmpEventFilter.so")
    
    gSystem.Load("libDmpKernel.so")
    gSystem.Load("libDmpService.so")

    ###Load DAMPE modules

    from ROOT import DmpChain, DmpEvent, DmpFilterOrbit, DmpPsdBase, DmpCore
    from ROOT import DmpSvcPsdEposCor, DmpVSvc   #DmpRecPsdManager
    import DMPSW

    for fIdx,file in enumerate(os.listdir(opts.input)):
        fNpath = str(opts.input) + "/" + str(file)
        DMPSW.IOSvc.Set("InData/Read" if fIdx == 0 else "InData/ReadMore",fNpath)
        if os.path.isfile(fNpath):
            mcChain.Add(fNpath)
            if opts.verbose:
                print('Adding {} to the chain...'.format(fNpath))

def readMC(opts,mcChain,nevents,eKinHisto,kStep):
    
    ###Load DAMPE libs

    gSystem.Load("libDmpEvent.so")
    gSystem.Load("libDmpEventFilter.so")
    
    gSystem.Load("libDmpKernel.so")
    gSystem.Load("libDmpService.so")

    ###Load DAMPE modules

    from ROOT import DmpChain, DmpEvent, DmpFilterOrbit, DmpPsdBase, DmpCore
    from ROOT import DmpSvcPsdEposCor, DmpVSvc   #DmpRecPsdManager
    import DMPSW
    
    if opts.verbose:
        print("Reading TChain data ...")
        if opts.debug:
            print('Debug mode activated... max mumber of events {}'.format(opts.debug))

    for idx in tqdm(range(nevents)):
        DmpVSvc.gPsdECor.SetMCflag(1)
        pev=mcChain.GetDmpEvent(idx)
        eKinHisto.Fill(pev.pEvtSimuPrimaries().pvpart_ekin)
        if eventProcess(opts,idx,nevents,kStep):
            break