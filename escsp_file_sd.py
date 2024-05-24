from escsp import *
import glob
import os
import math

############################################
#
drive_path=""
drive_names=[""]
data_path=""
audiomoth_spreadsheet=""
config_name="CONFIG.TXT"
############################################

#Reads the master audiomoth spreadsheet, in csv format
# and returns a Pandas dataframe
audiomoth_info=escsp_read_audiomoth_csv(audiomoth_spreadsheet)

drives=glob.glob(drive_path)

sd_name=""
error_conditions={"No SD Card":0,
                  "Serial Number not found":0}

for drive in drives:
    for drive_name in drive_names:
        if drive != drive_name: sd_name= drive

if sd_name == "":error_conditions["No SD Card"]=1

if sd_name != "":
    sd_info=escsp_read_audiomoth_config(os.path.join())
    # making boolean series for the serial number
    filter = audiomoth_info["serial_number"] == sd_info["serial_number"]
 
    # filtering data.  ams -> AudioMoth Spreadsheet
    ams_row=audiomoth_info.audiomoth_info(filter)
    if math.isnan(ams_row["ESID"]):error_conditions["Serial Number not found"]=1
    else:
       


else: