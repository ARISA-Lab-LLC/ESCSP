#generate_reports_1.py
"""Script to generate a Reports_1.csv file if given a top level folder that contains
    ESID Folders."""

##########################################################
#Import Libaries
from escsp import *
import os
##########################################################
#Set global variables
#top_directory="/media/tracy/ESCSPA00/Total_Raw_Data/"
top_directory="/media/tracy/SIU_PEASE01/"
#outname="Report_1.csv"
outname="Report_1_pease.csv"
##########################################################
folders=get_es_folder_list(top_directory, verbose=False, split = False)

dfs=[]
for folder in folders:
    dfs.append(Reports_1(folder, TOTAL=True))

combined_df = pd.concat(dfs, ignore_index=True)
combined_df.to_csv(os.path.join(top_directory, outname), index=False)
