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
plots_folder=os.path.join(top_directory,"Manual_PSD_Plots")
if not os.path.isdir(plots_folder):
    os.system('mkdir '+plots_folder)
#top_directory="/media/tracy/SIU_PEASE01/"
#outname="Report_1.csv"
# Get the current time
current_time = datetime.datetime.now()
# Format the current time as YYYY_MM_DD_hour_minute
formatted_time = current_time.strftime("%Y%m%d_%H%M")
outname=formatted_time+"_Manual_PSD.csv"
##########################################################
#folders=get_es_folder_list(top_directory, verbose=verbose, split = True)
#print(len(folders))
folders=[]
good_sites=["ESID#002_AnnularEclipse_AudioMothTimeChime_Split",
            "ESID#004_AnnularEclipse_AudioMothTimeChime_Split",
            "ESID#015_AnnularEclipse_AudioMothTimeChime_Split",
            "ESID#078_AnnularEclipse_AudioMothTimeChime_Split",
            "",
            ""]

for folder in folders:
    print("")
    print("Folder: "+folder)
    escsp_get_psd(folder, plots_folder, filelist=None, eclipse_type = "Total", verbose=verbose)
   

