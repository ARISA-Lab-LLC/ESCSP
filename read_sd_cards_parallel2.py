#read_sd_cards.py

import pandas as pd
import os 
import shutil
import glob
import time
import concurrent.futures
from multiprocessing import Pool
from natsort import natsorted
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
verbose=True

#Define functions
def copy_sd_card_files(paths_dict):
    drive_path=paths_dict['drive_path']
    raw_data_path=paths_dict["raw_data_path"]
    if verbose: print(drive_path+" to "+raw_data_path)
    # Create a pattern to match all files in the given directory
    pattern = os.path.join(drive_path, '*')
    # Use glob to find all files matching the pattern
    files_to_copy = glob.glob(pattern)
    command_dict_list=[]
    for file_to_copy in files_to_copy:  
        if os.path.isfile(file_to_copy):
            temp={"raw_data_path":raw_data_path,
                  "file_to_copy":file_to_copy}
            command_dict_list.append(temp)

            #if verbose: print("Copying "+file_to_copy+" to "+raw_data_path)
            #shutil.copy2(file_to_copy, raw_data_path)
            #if verbose: print("Copied "+file_to_copy+" to "+raw_data_path)

    p2=Pool(processes=5)
    p2.map_async(copy_command1, command_dict_list)
    p2.close()
    p2.join()
    return drive_path+" copied to "+raw_data_path

def copy_command1(command_dict):
    raw_data_path=command_dict["raw_data_path"]
    file_to_copy=command_dict["file_to_copy"]
    if verbose: print("Copying "+file_to_copy+" to "+raw_data_path+" using shutil.copy2")
    shutil.copy2(file_to_copy, raw_data_path)
    if verbose: print("Copied "+file_to_copy+" to "+raw_data_path)
    

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
current_drives=natsorted(current_drives)
for drive in current_drives:
    drive_path=os.path.join(drive_dir,drive)+"/"
    if verbose: print(drive_path)
    if drive_path in drive_list:
        if verbose: print(drive_path+" Skipped")
    else:
        if verbose: print("Operating on drive: "+drive_path)
        file_path=os.path.join(drive_path, "CONFIG.TXT")
        if verbose: print("file_path ="+ file_path)
        if os.path.exists(file_path):
            ESID=escsp_sn2esid(file_path, AM_df)
            if verbose: print("ESID "+ESID)
            SD_total, SD_used, SD_free = shutil.disk_usage(drive_path)
            free_space=0
            for out_drive in out_drive_list:
                if free_space == 0:
                    if drive_storage_dict[out_drive]["Storage Free"] > SD_used*1.01:
                        free_space=1
                        new_used=drive_storage_dict[out_drive]["Storage Free"]+SD_used
                        drive_storage_dict[out_drive]["Storage Free"]=new_used
                        if verbose: print("Saving to drive: "+out_drive)
                        raw_data_path=os.path.join(out_drive, save_dir, "ESID#"+ESID)
                        if verbose: print("Saving to drive: "+out_drive)
                        if os.path.isdir(raw_data_path):
                            raw_data_path=os.path.join(out_drive, save_dir, "ESID#"+ESID+"_"+drive)
                        os.mkdir(raw_data_path)
                        paths_dict_list.append({"raw_data_path":raw_data_path,
                                                "drive_path":drive_path})
                    else: 
                        if verbose: print("Drive "+out_drive+ "is full.  Moving to the next drive.")


        else:
            if verbose: print("No CONFIG.TXT file named "+file_path)
if verbose: print("length of paths_dict_list"+str(len(paths_dict_list)))

for path_dict in paths_dict_list:
    copy_sd_card_files(path_dict)

#p1=Pool(10)
#p1.map_async(copy_sd_card_files, paths_dict_list)
#p1.close()
#p1.join()


#with concurrent.futures.ThreadPoolExecutor() as executor:
#    futures = []
#    for paths_dict in paths_dict_list:
#        futures.append(executor.submit(copy_sd_card_files(paths_dict)))
#    for future in concurrent.futures.as_completed(futures):
#        print(future.result())

#for paths_dict in paths_dict_list:
#    t1b=time.perf_counter()
#    copy_sd_card_files(paths_dict)
#    t2b=time.perf_counter()
#    print(f'It took: {t2b - t1b} seconds to copy {str(paths_dict["drive_path"])} ')
#    print(f'It took: {(t2b - t1b)/60.} minutes to copy {str(paths_dict["drive_path"])} ')

t2a=time.perf_counter()
if verbose: print(f'Code Took a total of: {t2a - t1a} seconds for {str(len(paths_dict_list))} drives')
if verbose: print(f'Code Took a total of: {(t2a - t1a)/60.} minutes for {str(len(paths_dict_list))} drives')
