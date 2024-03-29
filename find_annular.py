#find_annular.py

import csv
import pandas as pd
from escsp import *
import os


Volume="/media/tracy/Soundscape1/"
#Volume="/Volumes/Soundscape1/"

top_dir=Volume+"Annular_DATA/"
annular_spreadsheet=top_dir+"Spreadsheets/Annular_eclipse_data.csv"
spreadsheet_name="Spreadsheets/eclipse_data.csv"
#read the spreadsheet into a dataframe
df=pd.read_csv(annular_spreadsheet, header=[0])

#Only select the annular eclipses
df=df[df["LocalType"] == "Annular"]
ESIDs=df['ESID'].values.tolist()

#Get the site folders
folders=get_es_folder_list(top_dir, split=1)
#Get the ESID from the folder name

file2=open(os.path.join(top_dir, "annular_list.csv"), 'w')

index=0
for ESID in ESIDs:
    for folder in folders :
        #Get the ESID from the folder name
        print(folder)
        folder_id=int(filename_2_ESID(folder))
        
        if folder_id == int(ESID):
            df.iloc[index, : ].to_csv(os.path.join(folder,spreadsheet_name))
            file2.write(str(ESID)+","+folder+"\n")
    index +=1 
    print(index)

    #print(data_frame.iloc[data_frame.index[index]].at['Latitude']
    #      + data_frame.iloc[data_frame.index[index]].at['Longitude']
    #      + data_frame.iloc[data_frame.index[index]].at['Start time\n(Recorded by user)'])

file2.close()