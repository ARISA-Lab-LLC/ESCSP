#es_analyze.py

from escsp import *
import os
import datetime
import glob

Volume="/media/tracy/Soundscape1/"
#Volume="/Volumes/Soundscape1/"

top_level_directory=os.path.join(Volume, "/Annular_DATA/")
top_level_directory=Volume+"/Annular_DATA/"
print("top_level_directory: "+top_level_directory)
#plots_folder=os.path.join(top_level_directory, "/Plots") 
plots_folder=top_level_directory + "/Plots"
outfile=top_level_directory+"/Spreadshhets/ES_data_test.csv"
verbose=1# False
folders = get_es_folder_list(top_level_directory,  split = 1)
filelist=outfile

if verbose : print(folders)


counter = 0
for folder in folders:
        
    escsp_get_psd(folder, plots_folder, filelist=outfile, verbose=1)


    
        

