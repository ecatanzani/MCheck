def createOutDir(opts):
    import os

    wDir = os.getcwd()
    outPathDir = wDir + "/outFiles"

    if not os.path.isdir(outPathDir):  # Check if the out directory exists or not
        try:
            os.mkdir(outPathDir)
        except OSError:
            print('Creation of the output directory {} failed'.format(outPathDir))
            raise
        else:
            if opts.verbose:
                print('Succesfully created output directory: {}'.format(outPathDir))
    else:
        if opts.verbose:
            print('Using existing output path directory: {}'.format(outPathDir))
    return outPathDir


def createOutROOTFile(opts):
    from ROOT import TFile
    if not opts.output:
        rootOutPath = createOutDir(opts) + "/MCheck.root"
        defUsed = True
    else:
        rootOutPath = opts.output
        defUsed = False

    try:
        outFile = TFile(rootOutPath, "RECREATE")
    except OSError:
        print('Error writing output file {}'.format(opts.output))
    else:
        if defUsed:
            if opts.verbose:
                print('Default output ROOT file has been created: {}'.format(
                    rootOutPath))
        else:
            if opts.verbose:
                print('Output ROOT file has been created: {}'.format(rootOutPath))
    return outFile


def skippedOutFile(opts):
    outSkipped = createOutDir(opts) + "/skippedFiles.txt"
    try:
        skFile = open(outSkipped, "w+")
    except OSError:
        print('Error writing output skipped file {}'.format(outSkipped))
        raise
    else:
        if opts.verbose:
            print('Output skipped file has been created: {}'.format(outSkipped))
    return skFile


def writeSkipped(skFile, inFile, opts):
    skFile.write("%s\n" % inFile)
    if opts.verbose:
        print('Added {} to the skipped files'.format(inFile))


def eventProcess(opts, evIdx, totEvents, kStep=1):
    kBreak = False
    if opts.verbose:
        if opts.debug:
            if (evIdx % ((opts.debug)/10)) == 0 and evIdx != 0:
                print('\tProcessed event {} of {}'.format(evIdx, totEvents))
            if evIdx == (opts.debug-1):
                print('\tProcessed event {} of {}'.format(evIdx+1, totEvents))
                kBreak = True
        else:
            if (evIdx % kStep) == 0 and evIdx != 0:
                print('\tProcessed event {} of {}'.format(evIdx, totEvents))
    return kBreak
