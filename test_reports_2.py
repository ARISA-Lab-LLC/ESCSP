#test_reports_2.py
"""Script to generate a Reports_2.csv file if given a top level folder that contains
    ESID Folders."""

##########################################################
#Import Libaries
from escsp import *
import os
##########################################################
#Set global variables
top_directory="/media/tracy/ESCSPA00/Annular_Raw_Data/"
outname="test_Report_2.csv"
##########################################################
folders=get_es_folder_list(top_directory, verbose=False, split = False)
#folder=os.path.join(top_directory,"ESID#001")
#dfs=[]
df=Reports_2(folder, TOTAL=False)
df.to_csv(os.path.join(top_directory, outname), index=False)

