from ROOT import gSystem


def addToChain(opts, mcChain):

    # Load DAMPE libs

    gSystem.Load("libDmpEvent.so")
    gSystem.Load("libDmpKernel.so")
    gSystem.Load("libDmpService.so")

    # Load DAMPE modules
    import DMPSW
    import os

    from stuff import skippedOutFile, writeSkipped

    firstSkipped = True

    if not opts.list:
        if opts.verbose:
            print('Reading input ROOT files from dir: {}'.format(opts.input))
        for fIdx, file in enumerate(os.listdir(opts.input)):
            fNpath = str(opts.input) + "/" + str(file)
            DMPSW.IOSvc.Set("InData/Read" if fIdx ==
                            0 else "InData/ReadMore", fNpath)
            if os.path.isfile(fNpath):
                mcChain.Add(fNpath)
                if opts.verbose:
                    print('Adding {} to the chain...'.format(fNpath))
            else:
                if firstSkipped:
                    skFile = skippedOutFile(opts)
                    firstSkipped = False
                else:
                    writeSkipped(skFile, fNpath, opts)

    else:
        if opts.verbose:
            print('Reading input ROOT files from list: {}'.format(opts.list))
            files = [f.replace("\n", "")
                     for f in open(opts.list, 'r').readlines()]
            for idxFile, f in enumerate(files):
                DMPSW.IOSvc.Set("InData/Read" if idxFile ==
                                0 else "InData/ReadMore", f)
                if os.path.isfile(f):
                    mcChain.Add(f)
                    if opts.verbose:
                        print('Adding {} to the chain...'.format(f))
                else:
                    if firstSkipped:
                        skFile = skippedOutFile(opts)
                        firstSkipped = False
                    writeSkipped(skFile, f, opts)

    if not firstSkipped:
        skFile.close()
    nevents = mcChain.GetEntries()
    if opts.verbose:
        print('Collected {} events ...'.format(nevents))

    return nevents


def readMC(opts, mcChain, nevents, eKinHisto, kStep):

    # Load DAMPE libs

    gSystem.Load("libDmpEvent.so")
    # gSystem.Load("libDmpEventFilter.so")

    gSystem.Load("libDmpKernel.so")
    gSystem.Load("libDmpService.so")

    # Load DAMPE modules

    from ROOT import DmpVSvc
    from tqdm import tqdm
    from stuff import eventProcess

    if opts.verbose:
        print("Reading TChain data ...")
        if opts.debug:
            print('Debug mode activated... max mumber of events {}'.format(opts.debug))

    for idx in tqdm(range(nevents)):
        DmpVSvc.gPsdECor.SetMCflag(1)
        pev = mcChain.GetDmpEvent(idx)
        eKinHisto.Fill(pev.pEvtSimuPrimaries().pvpart_ekin)
        if eventProcess(opts, idx, nevents, kStep):
            break
