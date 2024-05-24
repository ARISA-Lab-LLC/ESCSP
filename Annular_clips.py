#Annular_clips.py
from escsp import *
import os
#####################################################
top_dir="/media/tracy/Soundscape1/Annular_DATA/"

youtube_folder=top_dir+"YouTube/"

verbose=1
####################################################
#ESIDS=get_escspids_to_analyze(top_dir)
ESIDS=['002','138', '169', '015', '022','081','111', '112','136'] 

folders=[]
num=[]
for ESID in ESIDS:
    folder=top_dir+"ESID#"+ESID+"_AnnularEclipse_AudioMothTimeChime_Split/"
    if os.path.isdir(folder):
        folders.append(folder)
    print(num)
    
escsp_make_clips(folders, youtube_folder, verbose=verbose)



