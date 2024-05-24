import csv
import pandas as pd
import numpy as np 
import os 
from escsp import *

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

data_frame=pd.read_csv(AM_spreadsheet, header=None)
#Remove the first three rows of the dataframe which was the old header
data_frame=data_frame.iloc[3:]
#Create the new header

new_header = ['AudioMoth ES ID Number',
              "AudioMoth Serial #",
              "Recepient Type",
              "Annular 2023",
              "Total 2024", 
              "Recipient Name",
              "Recipient Address",
              "Sign-up Email",
              "MicroSD Card Received",
              "Incomplete",
              "Complete / Incomplete",
              "Required Data Collector Steps Complete?",
              "Location Latitude & Longitude Included (Mailer)",
              "Location Start & Stop Time Included (Mailer)",
              "Data Card Included (Mailer)",
              "AudioMoth Returned (Mailer)",
              "User Notes",
              "Survey Completed",
              "Location Latitude & Longitude Entered (Survey)",
              "Location Start & Stop Time Entered (Survey)",
              "Latitude",
              "Longitude",
              "Start date (Recorded by user)",
              "Start time (Recorded by user)",
              "Time Zone",
              "Uploaded to RFCx Arbimon",
              "AudioMoth Time Stamp Set  0 = No, 1 = yes",
              "Time set with Spreadsheet Data 0 = No, 1 = yes",
              "Time set with Enclosed Note Data 0 = No, 1 = yes",
              "Three Days of Data Recorded? (Two days before and Eclipse Day 0 = No, 1 = yes",
              "On Path 1= Yes, 0 = no",
              "Eclipse Type",
              "Eclipse Percent",
              "Total Eclipse Start UTC", 
              "Total Eclipse End UTC",
              "Max Eclipse Time UTC", ]
for col in data_frame.columns:
    print(col)

if len(new_header) != len(data_frame.columns):
        print("Length of new_header= "+str(len(new_header)))
        print("Length of data_frame.columns= "+str(len(data_frame.columns)))
        raise ValueError("Length of new_header must match the number of columns in the DataFrame")
    

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