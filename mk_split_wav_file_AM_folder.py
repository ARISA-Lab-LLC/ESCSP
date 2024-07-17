#mk_split_wav_file_AM_folder.py
##########################################################
#Import Libaries
from escsp import *
import os
import datetime
##########################################################
#Set global variables
top_directory="/media/tracy/ESCSPA00/Total_Raw_Data/"
top_out_directorty="/media/tracy/ESCSPA01/Total_Analysis_Data/"
verb=True
#suffix="_AnnularEclipse_AudioMothTimeChime_Split"
suffix="_TotalEclipse_AudioMothTimeChime_Split"
##########################################################
folders=get_es_folder_list(top_directory, verbose=False, split = False)

for folder in folders:
    #Test to see if the time chime is properly set in the folder. 
    if AM_timestamp_set(folder, verbose=False):
        #Create out folder
        path_chunks=folder.split('/')
        if path_chunks[len(path_chunks)-1][0:4] == 'ESID':
            outdir=os.path.join(top_out_directorty,path_chunks[len(path_chunks)-1]+suffix)
        else:
            if path_chunks[len(path_chunks)-2][0:4] == 'ESID':
                outdir=os.path.join(top_out_directorty,path_chunks[len(path_chunks)-2]+suffix)
            else:
                if path_chunks[len(path_chunks)-1][0:4] != '':
                    outdir=os.path.join(top_out_directorty,path_chunks[len(path_chunks)-1]+suffix)
                else:
                    outdir=os.path.join(top_out_directorty,path_chunks[len(path_chunks)-2]+suffix)
        
        if os.path.exists(outdir):
            print("Directory "+outdir+" already exists.")
            outdir=outdir+"_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            print("Creating directory "+outdir+" instead.")
            os.mkdir(outdir)
        else: os.mkdir(outdir)


        split_wave_files(folder, outdir, duration=60, verbose=verb)


