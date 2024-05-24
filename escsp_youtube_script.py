#escsp_youtube_script.py
###########################################################################
#Import Libraries section
import os  
import subprocess
import pandas as pd
import glob
import csv
###########################################################################
#python3 escsp_upload_youtube_video.py --file="example.mov" --title="Summer vacation in California"
#    --description="Had fun surfing in Santa Cruz" --keywords="surfing,Santa Cruz" --category="22" --privacyStatus="private"
top_dir="/Volumes/Austrian/Annular_DATA/"
#top_dir="/media/tracy/Soundscape1/Annular_DATA/"
youtube_folder=top_dir+"YouTube"
###########################################################################
upload_csv_files=glob.glob(os.path.join(youtube_folder,"*_youtube.csv"))
verbose=1
###########################################################################

upload_csv_files.remove(upload_csv_files[0])
upload_csv_files.remove(upload_csv_files[0])
for upload_csv_file in upload_csv_files : 

    df=pd.read_csv(os.path.abspath(upload_csv_file), header=[0])
    if verbose: print(df.columns.tolist())

    media_file_dir=os.path.dirname(df["file"][0])
    media_file_name=os.path.basename(df["file"][0])

    if media_file_dir != youtube_folder:
        media_file=os.path.join(media_file_dir,media_file_name)
    else: media_file=df["file"][0]

    media_file="/Volumes/Austrian/Annular_DATA/YouTube/ESID#169_Non-Eclipse-Day_2023-10-14_two_days_before_3minute.mp4"

    if verbose: print("media_file: "+media_file)

    category="28"

    call=     "python3 escsp_upload_youtube_video.py"
    call=call+" --file=\""+media_file+"\""
    call=call+" --title=\""+df["title"][0]+"\""
    call=call+" --description=\""+ df["description"][0]+"\""
    call=call+" --keywords=\""+df["keywords"][0]+"\""
    #call=call+" --category=\""+ str(df["category"][0])+"\""
    call=call+" --category=\""+ category +"\""
    call=call+" --privacyStatus=\""+ df["private"][0]+"\""

    if verbose: print(call)

    subprocess.call(call, shell = True) 



