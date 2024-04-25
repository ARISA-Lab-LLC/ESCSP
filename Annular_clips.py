#Annular_clips.py
from escsp import *

ESIDS=['002','138', '169', '015', '022','081','111', '112','136'] 

top_dir="/media/tracy/Soundscape1/Annular_DATA/"

analysis_folder=top_dir+"YouTube/"

folders=[]
for ESID in ESIDS:
    folder=top_dir+"ESID#"+ESID+"_AnnularEclipse_AudioMothTimeChime_Split/"
    num=ESID
    folders.append(folder)
    print(num)
    
escsp_make_clips(folders, analysis_folder, num)



