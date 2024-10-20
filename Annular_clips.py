#Annular_clips.py
from escsp import *
import os

import glob
#####################################################
#top_dir="/media/tracy/ESCSPA00/Annular_DATA/"
top_dir="/media/tracy/ESCSPA00/Annular_Analysis_Data/"
#top_dir="/Volumes/Austrian/Annular_DATA/"
eclipse_data_csv=os.path.join(top_dir, "Spreadsheets", "2023_Annular_Eclipse_eclipse_data_all.csv")

youtube_folder=top_dir+"YouTube_Queue/"

verbose=1
####################################################
#ESIDS=get_escspids_to_analyze(top_dir)
ESIDS=['002','138', '169', '015', '022','081','111', '112','136', '231' , '232'] 
ESIDS=['014'] 

#folders=[]
#for ESID in ESIDS:
#    folder=top_dir+"ESID#"+ESID+"_AnnularEclipse_AudioMothTimeChime_Split/"
#    if os.path.isdir(folder):
#        folders.append(folder)
#    print(ESID)
folders=glob.glob(os.path.join(top_dir,"*_Split"))
print(len(folders))
escsp_make_clips(folders, youtube_folder, verbose=verbose)



