
###########################################################################
#Import Libraries section
import os  
import subprocess
import pandas as pd
###########################################################################


top_dir="/media/tracy/Soundscape1/Annular_DATA/"
youtube_folder=top_dir+"YouTube/"
###########################################################################
upload_csv_files=glob.glob(os.path.join(youtube_folder,"*_youtube.csv"))
verbose=1
###########################################################################

for upload_csv_file in upload_csv_files : 
    if verbose: print(upload_csv_file)
    #df=pd.read_csv(upload_csv_file, header=[0])

