from ROOT import gSystem, gROOT

def addToChain(opts,mcChain):
    
    ###Load DAMPE libs

    gSystem.Load("libDmpEvent.so")
    #gSystem.Load("libDmpEventFilter.so")
    
    gSystem.Load("libDmpKernel.so")
    gSystem.Load("libDmpService.so")

    ###Load DAMPE modules

    from ROOT import DmpChain,DmpEvent,DmpCore,DmpVSvc
    import DMPSW
    import os

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
    #gSystem.Load("libDmpEventFilter.so")
    
    gSystem.Load("libDmpKernel.so")
    gSystem.Load("libDmpService.so")

    ###Load DAMPE modules

    from ROOT import DmpChain,DmpEvent,DmpVSvc
    from ROOT import TH1D
    import DMPSW
    from tqdm import tqdm
    from stuff import eventProcess

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