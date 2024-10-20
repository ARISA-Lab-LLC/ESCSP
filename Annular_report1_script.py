##########################################################
#Import Libaries
from escsp import *
import os
##########################################################
#Set global variables
#top_directory="/media/tracy/ESCSPA00/Total_Raw_Data/"
top_directory="/media/tracy/ESCSPA00/Annular_Raw_Data/"
data_analysis_dir="/media/tracy/ESCSPA00/Annular_Analysis_Data/"
eclipse_data_csv=os.path.join(data_analysis_dir, "Spreadsheets", "2023_Annular_Eclipse_eclipse_data_all.csv")

#outname="Report_1.csv"
# Get the current time
current_time = datetime.datetime.now()
# Format the current time as YYYY_MM_DD_hour_minute
formatted_time = current_time.strftime("%Y%m%d_%H%M")
outname1="Report_1_Annular_"+formatted_time+".csv"
outname2="Report_2_Annular_"+formatted_time+".csv"

verbose=1
##########################################################
folders=get_es_folder_list(top_directory, verbose=verbose, split = False)

dfs1=[]
dfs2=[]
for folder in folders:
    dfs1_temp=None
    dfs2_temp=None
    dfs1_temp=Reports_1(folder, TOTAL=False)
    if type(dfs1_temp).__name__ == 'DataFrame':
        dfs1.append(dfs1_temp)

    dfs2_temp=Reports_2(folder, eclipse_data_csv=eclipse_data_csv, TOTAL=False, verbose=verbose)
    if type(dfs2_temp).__name__ == 'DataFrame':
        dfs2.append(dfs2_temp)

combined_df1 = pd.concat(dfs1, ignore_index=True)
combined_df1.to_csv(os.path.join(top_directory, outname1), index=False)

combined_df2 = pd.concat(dfs2, ignore_index=True)
combined_df2.to_csv(os.path.join(top_directory, outname2), index=False)

