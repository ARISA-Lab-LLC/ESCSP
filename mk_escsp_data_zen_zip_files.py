#mk_escsp_data_zen_zip_files.py
###########################################################################
#Import Libraries section
from escsp import *
import os
import shutil 
import glob
###########################################################################
directory_in="/media/tracy/ESCSPA00/2024_Total_Raw_Data/"
#directory_in="/media/tracy/NEW_A1/2023_Annular_Raw_Data/"
directory_out="/media/tracy/ESCSPzip01/2024_Total_Raw_Data_ZIP/"
#directory_out="/media/tracy/ESCSPzip01/2023_Annular_Raw_Data_ZIP/"
zip_suffix=".zip "
zip_suffix=".zip "

#Define the folders to be Zipped
folders=glob.glob(os.path.join(directory_in,"ESID#*"))
#folders=[ "ESID#001",
#          "ESID#002",
#          "ESID#004",
#          "ESID#504",
#          "ESID#211"]
# Test
cwd = os.getcwd()

os.chdir(directory_in)
for folder in folders:
        
        in_path=os.path.join(directory_in, folder)
        if os.path.isdir(in_path):
            print("folder= "+folder)
            print("directory_out= "+directory_out)

            out_path=os.path.join(directory_out, folder.split("/")[-1]+zip_suffix)
            print("out_path= "+out_path)

            zip_command="zip -r " 
            zip_command=zip_command+out_path+ " "+folder
            zip_command=zip_command+" --exclude .Trash* --exclude .Trash*/* --exclude .Spotlight*"
            zip_command=zip_command+" --exclude .Spotlight*/* "
            zip_command=zip_command+" --exclude .* --exclude System* --exclude *Spotlight* --exclude *.fseventsd*"
            zip_command=zip_command+" --exclude 'System\ *' --exclude Sys*"

            print(zip_command)
            os.system(zip_command)    
                        
        else: print(in_path+" is not a valid directory")


os.chdir(cwd) 

print("done")
