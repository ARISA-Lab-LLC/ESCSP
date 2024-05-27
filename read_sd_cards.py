#read_sd_cards.py

import pandas as pd
import numpy as np 
import os 
import shutil
import subprocess
import glob
from escsp import *

#Get system environmental variables that may change from system to system
#Volume=os.getenv(ESCSP_Volume)
total_AM_spreadsheet=os.getenv("total_redacted_AM_spreadsheet")
drive_list_file=os.getenv("drive_list_file")
out_drive_list_file=os.getenv("out_drive_list_file")
drive_dir=os.getenv("drive_dir")

#Set other global variables
save_dir="Total_Raw_Data/"

AM_df=pd.read_csv(total_AM_spreadsheet, header=[0])
drive_list_df=pd.read_csv(drive_list_file, header=[0])
out_drive_list_df=pd.read_csv(out_drive_list_file, header=[0])

drive_list=drive_list_df["Drives"].to_list()
out_drive_list=out_drive_list_df["Drives"].to_list()

current_drives=os.listdir(drive_dir)

for drive in current_drives:
    drive_path=os.path.join(drive_dir,drive)+"/"
    print(drive_path)
    if drive_path in drive_list:
        print("...")
    else:
        file_path=os.path.join(drive_path, "CONFIG.TXT")
        if os.path.exists(file_path):
            ESID=escsp_sn2esid(file_path, AM_df)
            SD_total, SD_used, SD_free = shutil.disk_usage(drive_path)
            free_space=0
            for out_drive in out_drive_list:
                if free_space == 0:
                    D_total, D_used, D_free = shutil.disk_usage(out_drive)
                    if D_free > SD_used:
                        free_space=1
                        raw_data_path=os.path.join(out_drive, save_dir, "ESID#"+ESID)
                        if os.path.isdir(raw_data_path):
                            raw_data_path=os.path.join(out_drive, save_dir, "ESID#"+ESID+"_"+drive)
                        os.mkdir(raw_data_path)
                        # Create a pattern to match all files in the given directory
                        pattern = os.path.join(drive_path, '**', '*')
                        # Use glob to find all files matching the pattern
                        files_to_copy = glob.glob(pattern, recursive=True)
                        for file_to_copy in files_to_copy:
                            shutil.copy2(file_to_copy, raw_data_path)
                        #rsync_call="rsync -auv "+file_path+"/ "+raw_data_path
                        #rsync_result = subprocess.run(rsync_call, shell=True, capture_output=True, text=True)


        else:
            raise ValueError("No CONFIG.TXT file named "+file_path)
