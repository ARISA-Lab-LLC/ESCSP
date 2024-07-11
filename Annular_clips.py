#Annular_clips.py
from escsp import *
import os
#####################################################
#top_dir="/media/tracy/ESCSPA00/Annular_DATA/"
top_dir="/Volumes/Austrian/Annular_DATA/"
youtube_folder=top_dir+"YouTube/"

verbose=1
####################################################
#ESIDS=get_escspids_to_analyze(top_dir)
ESIDS=['002','138', '169', '015', '022','081','111', '112','136', '231' , '232'] 
ESIDS=['014'] 

folders=[]
for ESID in ESIDS:
    folder=top_dir+"ESID#"+ESID+"_AnnularEclipse_AudioMothTimeChime_Split/"
    if os.path.isdir(folder):
        folders.append(folder)
    print(ESID)
    
escsp_make_clips(folders, youtube_folder, verbose=verbose)



