from stuff import createOutDir
from writeList import writeListToFile


def parseInputList(opts):
    outDir = createOutDir(opts)
    inputList = open(opts.list, 'r')
    listIdx = 0
    dataList = []
    for idx, fileName in enumerate(inputList):
        dataList.append(fileName.rstrip('\n'))
        if len(dataList) == opts.fileNumber:
            writeListToFile(opts, dataList, outDir, listIdx)
            dataList.clear()
            listIdx += 1
    if len(dataList) is not 0:
        writeListToFile(opts, dataList, outDir, listIdx)
        dataList.clear()
        listIdx += 1
    return listIdx, outDir
