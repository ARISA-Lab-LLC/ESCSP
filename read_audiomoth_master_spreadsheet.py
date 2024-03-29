import csv
import pandas as pd
import numpy as np 
import os 

Volume="/media/tracy/Soundscape1/"
#Volume="/Volumes/Soundscape1/""

AM_spreadsheet=Volume + "/Annular_DATA/AudioMoth_ES_ID.csv"
out_spreadsheet=Volume + "/Annular_DATA/lat_longs.csv"
esid_spreadsheet=Volume +"/Annular_DATA/analysis_esids.csv" 
#with open(AM_spreadsheet, mode ='r') as file:    
#       csvFile = csv.DictReader(file)
#       for row in csvFile:
#            print(lines)

lat_long_out=open(out_spreadsheet, "w")
esid_out=open(esid_spreadsheet, "w")

data_frame=pd.read_csv(AM_spreadsheet, header=[0,1,2])
ESID=data_frame['AudioMoth ES ID Number'].values.tolist()
lats=data_frame['Latitude'].values.tolist()
longs=data_frame['Longitude'].values.tolist()
times=data_frame['Start time\n(Recorded by user)'].values.tolist()

esid_out.write("ESID")

print_index=0
for index, row in data_frame.iterrows():
    if str(lats[index][0]) !=  'nan' and str(longs[index][0]) != 'nan':
        print(str(int(ESID[index][0]))+","+str(lats[index][0])+","+str(longs[index][0])+","+str(times[index][0]))
        if print_index !=0: 
            lat_long_out.write("\n")
            
        lat_long_out.write(str(lats[index][0])+","+str(longs[index][0]))
        esid_out.write("\n")
        esid_out.write(str(int(ESID[index][0])))
        print_index+=1
    #print(data_frame.iloc[data_frame.index[index]].at['Latitude']
    #      + data_frame.iloc[data_frame.index[index]].at['Longitude']
    #      + data_frame.iloc[data_frame.index[index]].at['Start time\n(Recorded by user)'])
    #print("")
    #print("")
esid_out.close()
lat_long_out.close()
#file.close()