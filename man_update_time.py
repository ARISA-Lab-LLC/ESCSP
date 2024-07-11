#man_update_time.py
from escsp import *
import os
import datetime
import shutil


Volume="/Volumes/ESCSPF00/"
top_in_dir=os.path.join(Volume, "Total_Raw_Data")
top_out_dir=os.path.join(Volume,"Total_Time_Adjusted_Data" )
in_dir=os.path.join(top_in_dir, "ESID#232")
out_dir=os.path.join(top_out_dir, "ESID#232")
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

files=["19700103_074018.WAV",
       "19700103_200600.WAV",
       "19700104_083141.WAV",
       "19700104_205722.WAV",
       "19700105_092303.WAV",
       "19700105_214844.WAV",
       "19700106_101425.WAV",
       "19700106_224006.WAV",
       "19700107_110547.WAV",
       "19700107_233128.WAV"]

AM_start_time=filename_2_datetime(files[0], type="AudioMoth")[0]
format="%Y%m%d_%H%M%S"
Actual_start_time_utc="20240405_202000"

Actual_start_time_utc_dt=datetime.datetime.strptime(Actual_start_time_utc, format)

delta=Actual_start_time_utc_dt-AM_start_time

for file in files:
    update_time=filename_2_datetime(file, type="AudioMoth")[0]+delta
    outfile=update_time.strftime(format)+".WAV"
    
    shutil.copy2(os.path.join(in_dir, file), os.path.join(out_dir, outfile))
    