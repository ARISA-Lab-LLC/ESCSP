#ESCSP_Analysis_01.py

import librosa
import librosa.display
import numpy as np

import os
import matplotlib.pyplot as plt
import birdnetlib
from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
#from birdnetlib.analyzer_lite import LiteAnalyzer
from datetime import datetime
from pathlib import Path
from birdnetlib import Recording
import pandas as pd
from escsp import * 

Base_dir="/media/tracy/ESCSPA03/2024_Total_Eclipse_Data_Terk/"
folders=["ESID#516",
         "ESID#517",
         "ESID#518"
         ]

Lats=[29.34487,
      29.345988,
      29.35396]
Longs=[-99.983234,
       -99.97628,
       -99.968933]

index=0
for folder in folders:
# ✅ Create empty DataFrame with no rows, no columns
    df = pd.DataFrame() 

#Find all of the wave files in the folder

    input_files=glob.glob(os.path.join(Base_dir,folder,"*."+"WAV"))
    input_files=natsorted(input_files)
    for input_file in input_files:

        obs_start_time=filename_2_datetime(input_file,
                                           file_type="AudioMoth", 
                                           verbose=False)[0]
# Load and initialize the BirdNET-Lite models.
#analyzer = LiteAnalyzer()
        analyzer = Analyzer()
        recording = Recording(
            analyzer,
            input_file,
            lat=Lats[index],
            lon=Longs[index],
            date=obs_start_time, 
            min_conf=0.25,
        )
        recording.analyze()
        print(recording.detections) # Returns list of detections.
# Convert detections to pandas DataFrame
        if df.empty:
            df = pd.DataFrame(recording.detections)
        else:
            df_temp=pd.DataFrame(recording.detections)
            df = pd.concat([df, df_temp], ignore_index=True)

# Preview the DataFrame structure
    print(df.head())
# Save DataFrame to CSV
    output_file=os.path.join(Base_dir, f"{folder}_species_list.csv")

    df.to_csv(output_file, index=False)
    print("Saved detections to " + output_file)
    index+=1

