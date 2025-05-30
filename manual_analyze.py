#manual_analyze.py
##########################################################
#Import Libaries
from escsp import *
import os
import datetime                                       

##########################################################
#Set global variables
Volume="/media/tracy/ESCSPA00"
#Volume="/Volumes/ESCSPA00"
Annular=True
Total=False
verbose=1# False
Test= False

ESID_list=[
    "002",
    "004",
    "015",
    "078",
    "110"
    "111",
    "112",
    "138",
    "141",
    "153",
    "157",
    "161",
    "164",
    "165",
    "169",
    "171",
    "231",
    "232"
    ]

#Annular Eclipse
if Annular:
    top_folder="Annular_Analysis_Data"
    eclipse_type = "Annular"
    top_level_directory=os.path.join(Volume,top_folder)
    eclipse_data_csv=os.path.join(top_level_directory, "Spreadsheets", "2023_Annular_Eclipse_eclipse_data_all.csv")
    column_text="ESID,"
    column_text=column_text+"All Frequencies: 10/12/2023 V^2,"
    column_text=column_text+"All Frequencies: 10/13/2023 V^2,"
    column_text=column_text+"All Frequencies: Average V^2 of 10/12 & 10/13,"
    column_text=column_text+"All Frequencies: Standard Deviation 10/12 & 10/13,"
    column_text=column_text+"All Frequencies: Annular Eclipse 10/12/2023 V^2,"	
    column_text=column_text+"All Frequencies: Difference /Standard Deviation (Annular Eclipse vs Average),"
    column_text=column_text+"Cricket Frequencies: 10/12/2023 PSD,"
    column_text=column_text+"Cricket Frequencies: 10/13/2023 PSD,"
    column_text=column_text+"Cricket Frequencies: Average V^2 of 10/12 & 10/13,"
    column_text=column_text+ "Cricket Frequencies: Standard Deviation 10/12 & 10/13,"
    column_text=column_text+"Cricket Frequencies: Eclipse 10/12/2023 V^2," 
    column_text=column_text+"Cricket Frequencies: Difference / Standard Deviation (Annular Eclipse vs Average) >2 Significant Increase <-2 Significant Increase"
    column_text=column_text+"\n"

#Total Eclipse
if Total:
    top_folder="Total_Analysis_Data"
    eclipse_type = "Total"
    top_level_directory=os.path.join(Volume,top_folder)
    eclipse_data_csv=os.path.join(top_level_directory, "Spreadsheets", "2024_Total_Eclipse_eclipse_data_all.csv")
    column_text="ESID,"
    column_text=column_text+"All Frequencies: 4/6/2024 V^2,"
    column_text=column_text+"All Frequencies: 4/7/2024 V^2,"
    column_text=column_text+"All Frequencies: Average V^2 of 4/6 & 4/7,"
    column_text=column_text+"All Frequencies: Standard Deviation 4/6 & 4/7,"
    column_text=column_text+"All Frequencies: Eclipse 4/8/2024 V^2,"	
    column_text=column_text+"All Frequencies: Difference / Standard Deviation (Eclipse vs Average),"
    column_text=column_text+"Cricket Frequencies: 4/6/2024 PSD,"
    column_text=column_text+"Cricket Frequencies: 4/7/2024 PSD,"
    column_text=column_text+"Cricket Frequencies: Average V^2 of 4/6 & 4/7,"
    column_text=column_text+ "Cricket Frequencies: Standard Deviation 4/6 & 4/7,"
    column_text=column_text+"Cricket Frequencies: Eclipse 4/8/2024 V^2," 
    column_text=column_text+"Cricket Frequencies: Difference / Standard Deviation (Eclipse vs Average) >2 Significant Increase <-2 Significant Increase"
    column_text=column_text+"\n"


spreadsheets_folder=os.path.join(top_level_directory, "Spreadsheets")
wave_folder=os.path.join(top_level_directory, "Files_to_Analyze")
if not os.path.exists(wave_folder):
    os.system("mkdir "+wave_folder)

plots_folder=os.path.join(top_level_directory, "Plots") 
outfile=os.path.join(spreadsheets_folder,"ES_data_test.csv")
relative_psd_csv_file=os.path.join(spreadsheets_folder,"Relative_PSD_data.csv")
new_relative_psd_csv=os.path.join(spreadsheets_folder,"New_Relative_PSD_data.csv")
if os.path.exists(new_relative_psd_csv):
    os.system("rm "+new_relative_psd_csv)
folders = get_es_folder_list(top_level_directory,  split = 1)
filelist=outfile

#folders=[os.path.join(top_level_directory,"ESID#201_TotalEclipse_AudioMothTimeChime_Split"),
#         os.path.join(top_level_directory,"ESID#232_TotalEclipse_AudioMothTimeChime_Split")
#         ]

##########################################################
if verbose : print(folders)

current_time = datetime.datetime.now()
# Format the current time as YYYY_MM_DD_hh_mm
formatted_time = current_time.strftime("%Y_%m_%d_%H_%M")
psd_file=os.path.join(spreadsheets_folder, formatted_time+"_PSD_analysis.csv")
if os.path.exists(psd_file):
     os.system("rm "+psd_file)

f = open(psd_file, "w")
f.write(column_text)
#f.close()
##########################################################

for ESID in ESID_list:
    folder=os.path.join("/media/tracy/ESCSPA00/Annular_Analysis_Data","ESID#"+ESID+"_AnnularEclipse_AudioMothTimeChime_Split" )
    print("Current Folder: ")
    print(folder)
    print(" ")
    #psd_file=os.path.join(top_level_directory, "Spreadsheets", "PSD_analysis.csv")
    psd_file=os.path.join(spreadsheets_folder, "old_"+formatted_time+"ESID#"+ESID+"_PSD_analysis.csv")

    psd_text=escsp_get_psd(folder, plots_folder, filelist=None, 
                           eclipse_type = eclipse_type, verbose=1, 
                           eclipse_data_csv=eclipse_data_csv,
                           relative_psd_csv=relative_psd_csv_file,
                           new_relative_psd_csv=new_relative_psd_csv,
                           spreadsheets_folder=spreadsheets_folder,
                           wave_folder=wave_folder
                           )
    #f = open(psd_file, "a")
    f.write(psd_text)
    
    
f.close()


    
        

