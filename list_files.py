#list_files.py
import os
import glob
import pandas as pd

directory ="/media/tracy/ESCSPA00/Annular_Raw_Data"
directory="/media/tracy/ESCSPA00/Total_Raw_Data"
outname="Total_Raw_list_2.csv"


files=glob.glob(os.path.join(directory, "*ESID*"))

numbers=[]
for file in files:
    number=file.replace("ESID#", '')
    number=number.replace(directory, '')
    number=number.replace('/', '')
    numbers.append(number)
    print(number)

df=pd.DataFrame({"ESIDs":numbers})

df.to_csv(outname, index=False)