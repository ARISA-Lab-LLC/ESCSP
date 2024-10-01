#generate_psds_1.py
"""Script to generate PSD if given a top level folder that contains
    ESID Folders."""

##########################################################
#Import Libaries
from escsp import *
import os
##########################################################
#Set global variables
verbose=1
top_directory="/media/tracy/ESCSPA00/Annular_Analysis_Data/"
plots_folder=os.path.join(top_directory,"Plots")
#top_directory="/media/tracy/SIU_PEASE01/"
#outname="Report_1.csv"
outname="Report_1.csv"
##########################################################
folders=get_es_folder_list(top_directory, verbose=verbose, split = True)
print(len(folders))

for folder in folders:
    print("")
    print("Folder: "+folder)
    escsp_get_psd(folder, plots_folder, filelist=None, eclipse_type = "Total", verbose=verbose)
   

