import os


def createSubFiles(opts, condorDirs):
    for cDir in condorDirs:
        os.chdir(cDir)

        # Find HTCondor python executable
        exePy = os.getcwd()
        exePy, sep, tail = exePy.partition('/Assets')
        exePy += "/validate.py"

        # Find executable arguments
        if opts.input:
            cFlag = "i"
            cInput = opts.input
        if opts.list:
            cFlag = "l"
            cInput = opts.list

        # Using default value for output file
        # Using verbose mode

        # Find lop path
        outputPath = os.getcwd() + "/" + "output.log"
        logPath = os.getcwd() + "/" + "output.clog"
        errPath = os.getcwd() + "/" + "output.err"

        # Sub file path
        subPath = os.getcwd() + "/" + "crawler.sub"
        
        # Writing sub file
        outSub = open(subPath, 'w+')
        outSub.write("universe = vanilla\n")
        outSub.write("executable = %s\n" % exePy)
        outSub.write("arguments = -%s %s -v\n" % (cFlag, cInput))
        outSub.write("output = %s\n" % outputPath)
        outSub.write("error = %s\n" % errPath)
        outSub.write("log = %s\n" % logPath)
        outSub.write("ShouldTransferFiles = YES\n")
        outSub.write("WhenToTransferOutput = ON_EXIT\n")
        outSub.write("queue 1")
        outSub.close()
        if opts.verbose:
            print('HTCondor sub file created: {}'.format(subPath))
