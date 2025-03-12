import os
import glob
import shutil
import subprocess


folder="/Volumes/Austrian/Annular_DATA/Files_to_Analyze"



files=glob.glob(os.path.join(folder,"*."+"WAV"))

for file in files:
    Call='ffmpeg -i '  + file +" -acodec mp3 " + os.path.splitext(file)[0]+".mp3"
    subprocess.call(Call, shell = True)