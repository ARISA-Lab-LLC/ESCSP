#escsp_data_test.py

from escsp import *
import os
import datetime
import glob
from escsp_get_psd import *


Volume="/media/tracy/Soundscape1/"
#Volume="/Volumes/Soundscape1/"

top_level_directory=os.path.join(Volume,"/Annular_Raw_Data/")
plots_folder=os.path.join(Volume, "/Annular_DATA/Plots/")
Spreadsheet_folder=os.path.join(Volume, "/Annular_DATA/Spreadsheets/")
outfile=os.path.join(Spreadsheet_folder, "ES_data_test.csv")
outfile2=os.path.join(Spreadsheet_folder, "ES_time_chime_set.csv")
verbose=1# False
early_date=datetime.datetime(2023, 10, 1)

folders = get_es_folder_list(top_level_directory)

if verbose : print(folders)
ES_ID=[]
for folder in folders:
    ES_ID.append(filename_2_ESID(folder))

if verbose : print(ES_ID)

f = open(outfile, "w")
f.write("ES ID, Number of Files, Correct Time Chime, Time Not Set\n")

f2 = open(outfile2, "w")
f.write("ES ID\n")

time_chime_counter=0
counter = 0
for folder in folders:
    recording_files=glob.glob(os.path.join(folder,"*."+"WAV"))
    f.write(ES_ID[counter]+", "+str(len(recording_files))+", ")
    incorrect_time_counter=0
    correct_time_counter=0
    for file in recording_files: 
        if filename_2_datetime(file)[0] > early_date : correct_time_counter+=1 

        if filename_2_datetime(file)[0] < early_date : incorrect_time_counter+=1

    if correct_time_counter > incorrect_time_counter:
        f.write("1 , 0 \n")
        time_chime_counter+=1
        f2.write(ES_ID[counter]+", "+ str(len(recording_files))+ "\n")

    else:  f.write("0 , 1 \n")
    counter+=1
    #if filename_2_datetime(file)[0] > early_date :
    #    try :
    #        escsp_get_psd(folder, plots_folder, verbose=1)
    #    except: 
    #        print("Error on ESID#:"+str(ES_ID)+ " "+folder )


f.close()
f2.close()

    
        

