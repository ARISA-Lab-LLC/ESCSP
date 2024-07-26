#escsp_youtube_script.py
###########################################################################
#Import Libraries section
import os  
import subprocess
import pandas as pd
import glob
import shutil
import csv
import re
from escsp import *
###########################################################################
#python3 escsp_upload_youtube_video.py --file="example.mov" --title="Summer vacation in California"
#    --description="Had fun surfing in Santa Cruz" --keywords="surfing,Santa Cruz" --category="22" --privacyStatus="private"
#top_dir="/Volumes/Austrian/Dropbox/programs/ESCSP_Data/"
#top_dir="/media/tracy/Soundscape1/Annular_DATA/"
top_dir="/media/tracy/ESCSPA00/Annular_DATA/"
#top_dir="/media/tracy/ESCSPA01/Total_Analysis_Data/"
youtube_in_basename="YouTube_Queue"
youtube_folder=os.path.join(top_dir,youtube_in_basename)
youtube_folder_out=os.path.join(top_dir,"YouTube_Uploaded")
###########################################################################
upload_csv_files=glob.glob(os.path.join(youtube_folder,"*_youtube.csv"))
verbose=1
###########################################################################

#upload_csv_files.remove(upload_csv_files[0])
#upload_csv_files.remove(upload_csv_files[0])
#out_info=[]
if verbose : print(len(upload_csv_files)) 

for upload_csv_file in upload_csv_files : 

    df=pd.read_csv(os.path.abspath(upload_csv_file), header=[0])
    if verbose: print(df.columns.tolist())

    media_file_dir=os.path.dirname(df["file"][0])
    media_file_name=os.path.basename(df["file"][0])
    media_file_base=media_file_name.replace('.mp4','')
    media_file_base.strip()

    if media_file_dir != youtube_folder:
        media_file=os.path.join(media_file_dir,media_file_name)
    else: media_file=df["file"][0]


    if verbose: print("media_file: "+media_file)

    category="28"

    match = re.search("/YouTube/",media_file)
    if match != None : 
        media_file=media_file.replace("/YouTube/", "/"+youtube_in_basename+"/")
        if verbose: print("Updating old YouTube path")


    if verbose: print(media_file)
    call=     "python3 escsp_upload_youtube_video.py"
    call=call+" --file=\""+media_file+"\""
    call=call+" --title=\""+df["title"][0]+"\""
    call=call+" --description=\""+ df["description"][0]+"\""
    call=call+" --keywords=\""+df["keywords"][0]+"\""
    #call=call+" --category=\""+ str(df["category"][0])+"\""
    call=call+" --category=\""+ category +"\""
    call=call+" --privacyStatus=\""+ df["private"][0]+"\""

    if verbose: print(call)
    
    result=call_output=subprocess.run(call, shell = True, capture_output=True, text=True) 

    if result.stdout != '':
        err=1
        link=get_youtube_link(result.stdout)

        if link !=None:


            out_info={
                "stdout":result.stdout,
                "stderr":result.stderr,
                "link":link
                }
            out_info_df=pd.DataFrame([out_info])
            df=df.join(df, out_info_df)
            output_file_path = os.path.join(youtube_folder_out,'YoutTube_output.csv')
            if os.path.exists(output_file_path):
                out_info_df.to_csv(output_file_path,  mode='a', index=False, header=False)
            else:
                df.to_csv(output_file_path, index=False)

        
            media_files = glob.glob(os.path.join(youtube_folder, media_file_base+"*"))
            if verbose: print("Files to move", media_files)
 
            # iterate on all files to move them from the Queue folder to the Uploaded folder
            for file_path in media_files:
                dst_path = os.path.join(youtube_folder_out, os.path.basename(file_path))
                shutil.move(file_path, dst_path)
                if verbose: print(f"Moved {file_path} -> {dst_path}")

    else:
        print(result.stderr, result.stdout)
 






