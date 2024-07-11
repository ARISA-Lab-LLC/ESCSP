#es_analyze.py

from escsp import *
import os
import datetime
import glob

#Volume="/media/tracy/ESCSPF00/"
Volume="/Volumes/ESCSPF00/"

top_level_directory=os.path.join(Volume, "/Total_Analysis_Data/")
top_level_directory=Volume+"/Total_Analysis_Data/"
print("top_level_directory: "+top_level_directory)
#plots_folder=os.path.join(top_level_directory, "/Plots") 
plots_folder=top_level_directory + "/Plots"
outfile=top_level_directory+"/Spreadshhets/ES_data_test.csv"
verbose=1# False
folders = get_es_folder_list(top_level_directory,  split = 1)
filelist=outfile

#folders=[os.path.join(top_level_directory,"ESID#201_TotalEclipse_AudioMothTimeChime_Split"),
#         os.path.join(top_level_directory,"ESID#232_TotalEclipse_AudioMothTimeChime_Split")
#         ]

eclipse_type = "Total"

if verbose : print(folders)


counter = 0
for folder in folders:
    print("Current Folder: ")
    print(folder)
    print(" ")
    escsp_get_psd(folder, plots_folder, filelist=None, eclipse_type = eclipse_type, verbose=1)


    
        

