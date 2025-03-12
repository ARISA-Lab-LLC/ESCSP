import pandas as pd
import os  
import shutil
import glob

df_out_name="missing_data_report.csv"
df_in_name="missing_data_to_pease.csv"
df_in = pd.read_csv(df_in_name)


missing_ESIDs=df_in["AudioMoth ES ID Number"]
top_in_dir1="/media/tracy/ESCSPA00/Total_Raw_Data"
top_in_dir2="/media/tracy/ESCSPA01/Total_Raw_Data"
top_out_dir="/media/tracy/ESCSPB02/Total_Raw_Data"

path_exists=[]
number_of_files=[]
success=[]
success_binary_list=[]
if not os.path.isdir(top_out_dir):
    os.system("mkdir "+top_out_dir)

for ESID in missing_ESIDs:
    print(str(ESID).zfill(3))
    folder_name="ESID#"+str(ESID).zfill(3)

    in_path1=os.path.join(top_in_dir1,
                         folder_name
                         )

    in_path2=os.path.join(top_in_dir2,
                         folder_name
                         )
    
    out_path=top_out_dir
                            
    print(in_path1)
    print(out_path)  
    does_exist="No"
    success_binary=0
    file_num=0
    Successfully_copied="No"
    if os.path.isdir(in_path1):
        does_exist="Yes"
        #file_num=len(os.listdir(in_path1))
        file_num = len(glob.glob(os.path.join(in_path1, "*.WAV")))
        command_line="rsync -auv "+in_path1+" "+out_path
        print(command_line)
        #os.system(command_line)
    else:
        if os.path.isdir(in_path2):
            does_exist="Yes"
            #file_num=len(os.listdir(in_path2))
            file_num = len(glob.glob(os.path.join(in_path2, "*.WAV")))
            command_line="rsync -auv --exclude '.*' --exclude 'System*' "+in_path2+" "+out_path
            #os.system(command_line)

    path_exists.append(does_exist)
    number_of_files.append(file_num)
    success_binary_list.append(file_num)
    out_dir_name=os.path.join(out_path, folder_name)
    if os.path.isdir(out_dir_name):
        if len(glob.glob(os.path.join(in_path1, "*.WAV"))) == file_num:       
            Successfully_copied="Yes"
            success_binary=1

    #    if len(os.listdir(out_dir_name)) == file_num:
    #        Successfully_copied="Yes"

    

    success.append(Successfully_copied)
    success_binary_list.append(success_binary)

    do_it=False
    if os.path.isdir(in_path1) or os.path.isdir(in_path2):
        for item in os.listdir(out_dir_name):
            item_path = os.path.join(out_dir_name, item)
        
        # Check if the item is hidden (starts with a dot)
            if item.startswith('.') or item.startswith('System'):
                try:
                # If it's a file, remove it
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                        print(f"Removed hidden file: {item_path}")
                # If it's a directory, remove it along with all its contents
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                        print(f"Removed hidden folder: {item_path}")
                except Exception as e:
                    print(f"Error removing {item_path}: {e}")


df_out=pd.DataFrame({"ESID #":missing_ESIDs,
                         "Folder Exists?":path_exists,
                         "Number of files in DB match number of files in drive?":success,
                         "Number of .WAV files":number_of_files
                         })

df_out.to_csv(df_out_name)


    #os.system("mkdir "+wave_folder)