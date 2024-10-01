#mk_escsp_data_zip_files.py
###########################################################################
#Import Libraries section
from escsp import *
import os
import shutil 
directory1="/media/tracy/ESCSPA00/Total_Raw_Data/"
directory2="/media/tracy/ESCSPA01/Total_Analysis_Data/"
directory3="/media/tracy/ESCSPA03/Zip_Files/Total/"

new_suffix="_2024TotalEclipse_RawData"
time_chime_suffix="_TotalEclipse_AudioMothTimeChime_Split"
suffix2="_2024TotalEclipse_AudioMothTimeChime"
tar_suffix=".tar.gz "

#folders=[ "ESID#515",
#          "ESID#516",
#          "ESID#517",
#          "ESID#518",
#          "ESID#937"]
folders=[ "ESID#519"]

for folder in folders:
        path1=os.path.join(directory1, folder)
        if os.path.isdir(path1):
            path2=os.path.join(directory2, folder+time_chime_suffix)
            eclipse_data=os.path.join(path2, "eclipse_data.csv")
            if os.path.isfile(eclipse_data):
                 shutil.copy(eclipse_data, folder)
            path3=os.path.join(directory2, folder+suffix2)
            eclipse_data=os.path.join(path3, "eclipse_data.csv")
            if os.path.isfile(eclipse_data):
                 shutil.copy(eclipse_data, folder)

            path4=os.path.join(directory1, folder+new_suffix)
            mv_command="mv "+path1+" "+path4
            print(mv_command)
            os.system(mv_command)

            tar_command="tar --exclude='.Trash*' --exclude='.Trash*/*' --exclude='.Spotlight*' --exclude='.Spotlight*/*' "
            tar_command=tar_command+"-czvf "+os.path.join(directory3,folder+new_suffix+tar_suffix) 
            tar_command=tar_command+" "+path4
            print(tar_command)
            os.system(tar_command)    
                        
        else: print(path1+" is not a valid directory")

print("done")
