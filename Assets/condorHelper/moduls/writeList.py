def writeListToFile(opts, dataList, outDir, listIdx, singleListOutput=None):
    from stuff import getListPath

    listPath = getListPath(outDir, listIdx) + ".txt"
    if singleListOutput is not None:
        listPath = singleListOutput

    try:
        outList = open(listPath, 'w+')
    except OSError:
        print('Creation of the output data list {} failed'.format(listPath))
        raise
    else:
        for file in dataList:
            outList.write("\n%s" % file)
        outList.close()
        if opts.verbose:
            print('Created output list: {}'.format(listPath))
