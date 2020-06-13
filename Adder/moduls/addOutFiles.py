from ROOT import TFile, TH1D, TH2D, TGraph
import os


def compute_final_histos(condor_dir_list, opts):
    
    # Final energy histo
    h_ekin_histo = TH1D()

    for dIdx, tmp_dir in enumerate(condor_dir_list):
        tmp_dir += "/outFiles"
        tmp_dir_list = os.listdir(tmp_dir)
        for elm in tmp_dir_list:
            if elm.startswith("analysisOutFile_"):
                rFile_path = tmp_dir + "/" + elm

        # Open ROOT output file
        rFile = TFile.Open(rFile_path, "READ")
        if rFile.IsOpen():
            if opts.verbose:
                if dIdx == 0:
                    print('\nReading file {}: {}'.format((dIdx+1), rFile_path))
                else:
                    print('Reading file {}: {}'.format((dIdx+1), rFile_path))
        else:
            print('Error reading file {}: {}'.format((dIdx+1), rFile_path))
            sys.exit()
            
        h_ekin_histo_tmp = rFile.Get("eKinHisto")
        h_ekin_histo_tmp.SetDirectory(0)

        # Close output file
        rFile.Close()

        # Add histos
        if dIdx == 0:
            h_ekin_histo = h_ekin_histo_tmp.Clone("h_ekin_histo")
        else:
            h_ekin_histo.Add(h_ekin_histo_tmp)
    
    # Create output file for full histos
    fOut = TFile.Open(opts.output, "RECREATE")
    if fOut.IsOpen():
        if opts.verbose:
            print('Output TFile has been created: {}'.format(opts.output))
    else:
        print('Error creating output TFile: {}'.format(opts.output))
        sys.exit()
    
    # Write final histo
    h_ekin_histo.Write()

    # Closing output file
    fOut.Close()