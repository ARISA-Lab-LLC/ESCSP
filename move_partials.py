#move_partials.py
"""Script to move folders with a partial eclipse."""

##########################################################
#Import Libaries
from escsp import *
import os
##########################################################
#Set global variables
verbose=1
top_directory="/media/tracy/ESCSPA00/Annular_Analysis_Data/"
partial_directory="/media/tracy/ESCSPA00/Annular_Partial_Data/"
##########################################################
folders=get_es_folder_list(top_directory, verbose=verbose, split = True)
print(len(folders))

for folder in folders:
    print("")
    print("Folder: "+folder)
    eclipse_data_csv=os.path.join(folder, "eclipse_data.csv")
    if os.path.isfile(eclipse_data_csv) :
        df=pd.read_csv(eclipse_data_csv, header=[0])
        second_contact=df["SecondContactTimeUTC"].values[0]
        if second_contact == 0:
            mv_coomand="mv "+
            os.system(mv_coomand)
   

