#read_audiomoth_master_spreadsheet.py
import csv
import pandas as pd
import numpy as np 
import os 
from escsp import *

#Get system environmental variables that may change from system to system
#Volume=os.getenv(ESCSP_Volume)
AM_spreadsheet_in=os.getenv("AM_spreadsheet")
AM_spreadsheet_out=os.getenv("out_spreadsheet")
esid_spreadsheet=os.getenv("esid_spreadsheet")
out2_spreadsheet=os.getenv("esid_spreadsheet")

lat_long_out=open(out2_spreadsheet, "w")
esid_out=open(esid_spreadsheet, "w")

data_frame=pd.read_csv(AM_spreadsheet_in, header=None)
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
              "How many people completed every step of the role?",
              "Incomplete",
              "Complete / Incomplete",
              "Required Data Collector Steps Complete?",
              "Location Latitude & Longitude Included (Mailer)",
              "Location Start & Stop Time Included (Mailer)",
              "Data Card Included (Mailer)",
              "AudioMoth Returned (Mailer)",
              "User Notes",
              "Online Survey Completed",
              "Location Latitude & Longitude Entered (Survey)",
              "Location Start & Stop Time Entered (Survey)",
              "What does this mean for the project?",
              "Latitude",
              "Longitude",
              "Start date Recorded by user",
              "Start time Recorded by user",
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
              "Max Eclipse Time UTC", 
              "Upload Round"
              ]

if len(new_header) != len(data_frame.columns):
        print("Length of new_header= "+str(len(new_header)))
        print("Length of data_frame.columns= "+str(len(data_frame.columns)))
        raise ValueError("Length of new_header must match the number of columns in the DataFrame")
else:   
    data_frame.columns = new_header
    
#Sanitize the spreadsheet of PII
# Identify columns to remove
data_frame.drop(columns=["Recepient Type", 
                         "Recipient Name", 
                         "Recipient Name",
                         "Recipient Address",
                         "Sign-up Email",
                         "Recepient Type"],
                         inplace=True)

ESID=data_frame['AudioMoth ES ID Number'].values.tolist()
lats=data_frame['Latitude'].values.tolist()
longs=data_frame['Longitude'].values.tolist()
dates=data_frame["Start date Recorded by user"].values.tolist()
times=data_frame['Start time Recorded by user'].values.tolist()

print_index=0
indices_to_remove = data_frame[data_frame['AudioMoth ES ID Number'] == np.nan].index
print("indices_to_remove= " +str(len(indices_to_remove)))
data_frame = data_frame.drop(indices_to_remove)
indices_to_remove = data_frame[data_frame['AudioMoth ES ID Number'] == "TOTAL"].index
print("indices_to_remove= " +str(len(indices_to_remove)))
data_frame = data_frame.drop(indices_to_remove)

for index, row in data_frame.iterrows():
    print(row['AudioMoth ES ID Number'])
    print(type(row['AudioMoth ES ID Number']))
    if type(row['AudioMoth ES ID Number']) != type(1.0): 
          if row['AudioMoth ES ID Number'] != "TOTAL":
            print(row['AudioMoth ES ID Number'])
            print(type(row['AudioMoth ES ID Number']))
            print(row['AudioMoth Serial #'])
            print(type(row['AudioMoth Serial #']))

data_frame.to_csv(AM_spreadsheet_out)

esid_out.close()
lat_long_out.close()
#file.close()