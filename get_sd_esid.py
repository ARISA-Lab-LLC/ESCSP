#get_sd_esid.py
import pandas as pd
import os 
from natsort import natsorted
from escsp import *
#Get system environmental variables that may change from system to system
#Volume=os.getenv(ESCSP_Volume)
total_AM_spreadsheet=os.getenv("total_redacted_AM_spreadsheet")
drive_list_file=os.getenv("drive_list_file")
drive_dir=os.getenv("drive_dir")

verbose=True


AM_df=pd.read_csv(total_AM_spreadsheet, header=[0])
drive_list_df=pd.read_csv(drive_list_file, header=[0])
drive_list=drive_list_df["Drives"].to_list()

current_drives=os.listdir(drive_dir)
current_drives=natsorted(current_drives)

for drive in current_drives:
    drive_path=os.path.join(drive_dir,drive)+"/"
    if drive_path in drive_list:
        if verbose: print(drive_path+"Skipped")
    else:
        file_path=os.path.join(drive_path, "CONFIG.TXT")
        if os.path.isfile(file_path):
            print(escsp_sn2esid(file_path, AM_df))
