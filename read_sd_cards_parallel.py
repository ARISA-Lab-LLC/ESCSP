#read_sd_cards.py

import pandas as pd
import os 
import shutil
import glob
import time
from escsp import *

t1a=time.perf_counter()
#Get system environmental variables that may change from system to system
#Volume=os.getenv(ESCSP_Volume)
total_AM_spreadsheet=os.getenv("total_redacted_AM_spreadsheet")
drive_list_file=os.getenv("drive_list_file")
out_drive_list_file=os.getenv("out_drive_list_file")
drive_dir=os.getenv("drive_dir")

#Set other global variables
save_dir="Total_Raw_Data/"

#Define functions
def copy_sd_card_files(paths_dict):
    drive_path=paths_dict['drive_path']
    raw_data_path=paths_dict["raw_data_path"]
    # Create a pattern to match all files in the given directory
    pattern = os.path.join(drive_path, '**', '*')
    # Use glob to find all files matching the pattern
    files_to_copy = glob.glob(pattern, recursive=True)
    for file_to_copy in files_to_copy:
        if open.path.isfile(file_to_copy):
            shutil.copy2(file_to_copy, raw_data_path)

    return drive_path+" copied to "+raw_data_path

#Start Script
#Read the AudioMoth Spreadsheet to get the relationship between S/N and ESID#
AM_df=pd.read_csv(total_AM_spreadsheet, header=[0])
drive_list_df=pd.read_csv(drive_list_file, header=[0])
out_drive_list_df=pd.read_csv(out_drive_list_file, header=[0])

drive_list=drive_list_df["Drives"].to_list()
out_drive_list=out_drive_list_df["Drives"].to_list()

current_drives=os.listdir(drive_dir)

paths_dict_list=[]
#Create a nested dictionary to keep track of the Storage on each drive.
drive_storage_dict={}
for ii in range(len(out_drive_list)):
    total, used, free = shutil.disk_usage(out_drive_list[ii])
    drive_storage_dict[out_drive_list[ii]] = {
        "Storage Free":free
    }

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
                    if drive_storage_dict[out_drive]["Storage Free"] > SD_used*1.01:
                        free_space=1
                        raw_data_path=os.path.join(out_drive, save_dir, "ESID#"+ESID)
                        if os.path.isdir(raw_data_path):
                            raw_data_path=os.path.join(out_drive, save_dir, "ESID#"+ESID+"_"+drive)
                        os.mkdir(raw_data_path)
                        paths_dict_list.append({"raw_data_path":raw_data_path,
                                                "drive_path":drive_path})


        else:
            raise ValueError("No CONFIG.TXT file named "+file_path)
for paths_dict in paths_dict_list:
    t1b=time.perf_counter()
    copy_sd_card_files(paths_dict)
    t2b=time.perf_counter()
    print(f'It took :{t2b - t1b} seconds to copy {str(paths_dict["drive_path"])} ')
    print(f'It took :{(t2b - t1b)/60.} minutes to copy {str(paths_dict["drive_path"])} ')

t2a=time.perf_counter()
print(f'Code Took a total of :{t2a - t1a} seconds for {str(len(paths_dict_list))} drives')
