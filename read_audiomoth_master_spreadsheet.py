#read_audiomoth_master_spreadsheet.py
import pandas as pd
import numpy as np 
import os 
from escsp import *
verbose=False
Annular=False
#Get system environmental variables that may change from system to system
#Volume=os.getenv(ESCSP_Volume)
AM_spreadsheet_in=os.getenv("total_AM_spreadsheet")
AM_spreadsheet_out=os.getenv("out_spreadsheet")
esid_spreadsheet=os.getenv("esid_spreadsheet")
out2_spreadsheet=os.getenv("total_redacted_AM_spreadsheet")
data_frame=pd.read_csv(AM_spreadsheet_in, header=[0,1,2])

old_df=copy.deepcopy(data_frame)
#Remove the first three rows of the dataframe which was the old header
#data_frame=data_frame.iloc[3:]

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
              "Time set with Spreadsheet Data 0 = No, 1 = yes",
              "Time set with Enclosed Note Data 0 = No, 1 = yes",
              "AudioMoth Time Stamp Set  0 = No, 1 = Yes",
              "Data Uploaded? 0 = No, 1 = Yes",
              "Three Days of Data Recorded? (Two days before and Eclipse Day 0 = No, 1 = yes",
              "April 6, 2024 Data 0 = No, 1 = Yes",
              "April 7, 2024 Data 0 = No, 1 = Yes",
              "April 8, 2024 Data 0 = No, 1 = Yes",
              "April 9, 2024 Data 0 = No, 1 = Yes",
              "April 10, 2024 Data 0 = No, 1 = Yes",
              "April 11, 2024 Data 0 = No, 1 = Yes",
              "On Path 1= Yes, 0 = no",
              "Eclipse Type",
              "Eclipse Percent",
              "Total Eclipse Start UTC", 
              "Total Eclipse End UTC",
              "Max Eclipse Time UTC", 
              "Upload Round",
              "Unusable Data 1 = Unusable",
              "Manually Add ES ID# to Raw Data Upload 1 = Need to Do",
              "Audio Data YouTube Link", 
              "Not filtered (All frequencies), 4/6/2024 PSD",
              "Not filtered (All frequencies), 4/7/2024 PSD",
              "Not filtered (All frequencies), Average PSD of 4/6 & 4/7",
              "Not filtered (All frequencies), 4/8/2024 PSD",
              "Not filtered (All frequencies), Standard Deviation (Average vs Eclipse)",
              "Filtered (Cricket frequency), 4/6/2024 PSD",
              "Filtered (Cricket frequency), 4/7/2024 PSD",
              "Filtered (Cricket frequency), Average PSD of 4/6 & 4/7",
              "Filtered (Cricket frequency), eclipse 4/8/2024 PSD",
              "Filtered (Cricket frequency), Standard Deviation (Average vs Eclipse)",
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
if verbose: print("indices_to_remove= " +str(len(indices_to_remove)))
data_frame = data_frame.drop(indices_to_remove)
indices_to_remove = data_frame[data_frame['AudioMoth ES ID Number'] == "TOTAL"].index
if verbose: print("indices_to_remove= " +str(len(indices_to_remove)))
data_frame = data_frame.drop(indices_to_remove)

for index, row in data_frame.iterrows():
    if verbose: print(row['AudioMoth ES ID Number'])
    if verbose: print(type(row['AudioMoth ES ID Number']))
    if type(row['AudioMoth ES ID Number']) != type(1.0): 
          if verbose: 
            if row['AudioMoth ES ID Number'] != "TOTAL":
                print(row['AudioMoth ES ID Number'])
                print(type(row['AudioMoth ES ID Number']))
                print(row['AudioMoth Serial #'])
                print(type(row['AudioMoth Serial #']))
    if Annular:
         print("Annular")
    else:
        
        if row["Eclipse Percent"] >= 99.95:
             row["Eclipse Type"]="Total"
        else: row["Eclipse Type"]="Partial"
        

    

data_frame.to_csv(AM_spreadsheet_out)

#esid_out.close()
#lat_long_out.close()
#file.close()