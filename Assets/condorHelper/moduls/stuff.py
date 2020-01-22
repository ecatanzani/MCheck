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


def getListPath(outDir, listIdx):
    finaListPath = outDir + "/dataList_" + str(listIdx)
    return finaListPath