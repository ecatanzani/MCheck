import os
from stuff import createOutDir
from writeList import writeListToFile


def parseInputDir(opts, noSplitList=False, singleListOutput=None):
    if singleListOutput is None:
        outDir = createOutDir(opts)
    try:
        os.path.exists(opts.input)
    except OSError:
        print('Error retreaving input ROOT files from {}'.format(opts.input))
        raise
    else:
        if not noSplitList:
            homeWD = os.getcwd()
            os.chdir(opts.input)
            dataWD = os.getcwd()
            listIdx = 0
            dataList = []
            for idx, fileName in enumerate(os.listdir(dataWD)):
                completeFileName = dataWD + "/" + fileName
                dataList.append(completeFileName)
                if len(dataList) == opts.fileNumber:
                    writeListToFile(opts, dataList, outDir, listIdx)
                    dataList.clear()
                    listIdx += 1
            if len(dataList) is not 0:
                writeListToFile(opts, dataList, outDir, listIdx)
                dataList.clear()
                listIdx += 1
            os.chdir(homeWD)
        else:
            homeWD = os.getcwd()
            os.chdir(opts.input)
            dataWD = os.getcwd()
            relDataList = os.listdir(dataWD)
            relDataList = relDataList[:opts.fileNumber]
            prefix = dataWD + "/"
            os.chdir(homeWD)
            absDataList = [prefix + iFile for iFile in relDataList]
            print(os.getcwd())
            if singleListOutput is None:
                writeListToFile(opts, absDataList, outDir, 0, singleListOutput)
            else:
                writeListToFile(opts, absDataList, "", 0, singleListOutput)
