import shutil
import os

out_dir="/Volumes/ESCSPF00//Total_Analysis_Data/To_Google_Drive/"

if not os.path.isdir(out_dir):
    os.mkdir(out_dir)



files=[
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#201_TotalEclipse_AudioMothTimeChime_Split/20240408_185015.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#201_TotalEclipse_AudioMothTimeChime_Split/20240408_185115.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#201_TotalEclipse_AudioMothTimeChime_Split/20240408_185215.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#201_TotalEclipse_AudioMothTimeChime_Split/20240406_184931.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#201_TotalEclipse_AudioMothTimeChime_Split/20240406_185031.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#201_TotalEclipse_AudioMothTimeChime_Split/20240406_185131.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#201_TotalEclipse_AudioMothTimeChime_Split/20240406_185231.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#201_TotalEclipse_AudioMothTimeChime_Split/20240407_184953.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#201_TotalEclipse_AudioMothTimeChime_Split/20240407_185053.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#201_TotalEclipse_AudioMothTimeChime_Split/20240407_185153.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#201_TotalEclipse_AudioMothTimeChime_Split/20240407_185253.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#001_TotalEclipse_AudioMothTimeChime_Split/20240408_185019.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#001_TotalEclipse_AudioMothTimeChime_Split/20240408_185119.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#001_TotalEclipse_AudioMothTimeChime_Split/20240408_185219.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#001_TotalEclipse_AudioMothTimeChime_Split/20240406_184935.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#001_TotalEclipse_AudioMothTimeChime_Split/20240406_185035.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#001_TotalEclipse_AudioMothTimeChime_Split/20240406_185135.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#001_TotalEclipse_AudioMothTimeChime_Split/20240406_185235.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#001_TotalEclipse_AudioMothTimeChime_Split/20240407_184957.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#001_TotalEclipse_AudioMothTimeChime_Split/20240407_185057.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#001_TotalEclipse_AudioMothTimeChime_Split/20240407_185157.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#001_TotalEclipse_AudioMothTimeChime_Split/20240407_185257.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#015_TotalEclipse_AudioMothTimeChime_Split/20240408_184930.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#015_TotalEclipse_AudioMothTimeChime_Split/20240408_185030.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#015_TotalEclipse_AudioMothTimeChime_Split/20240408_185130.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#015_TotalEclipse_AudioMothTimeChime_Split/20240408_185230.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#015_TotalEclipse_AudioMothTimeChime_Split/20240406_184942.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#015_TotalEclipse_AudioMothTimeChime_Split/20240406_185042.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#015_TotalEclipse_AudioMothTimeChime_Split/20240406_185142.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#015_TotalEclipse_AudioMothTimeChime_Split/20240406_185242.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#015_TotalEclipse_AudioMothTimeChime_Split/20240407_185006.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#015_TotalEclipse_AudioMothTimeChime_Split/20240407_185106.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#015_TotalEclipse_AudioMothTimeChime_Split/20240407_185206.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#519_TotalEclipse_AudioMothTimeChime_Split/20240408_184935.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#519_TotalEclipse_AudioMothTimeChime_Split/20240408_185035.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#519_TotalEclipse_AudioMothTimeChime_Split/20240408_185135.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#519_TotalEclipse_AudioMothTimeChime_Split/20240408_185235.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#519_TotalEclipse_AudioMothTimeChime_Split/20240406_184948.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#519_TotalEclipse_AudioMothTimeChime_Split/20240406_185048.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#519_TotalEclipse_AudioMothTimeChime_Split/20240406_185148.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#519_TotalEclipse_AudioMothTimeChime_Split/20240406_185248.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#519_TotalEclipse_AudioMothTimeChime_Split/20240407_185011.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#519_TotalEclipse_AudioMothTimeChime_Split/20240407_185111.WAV",
    "/Volumes/ESCSPF00//Total_Analysis_Data/ESID#519_TotalEclipse_AudioMothTimeChime_Split/20240407_185211.WAV"
    ]

for file in files:
    sub_dir=os.path.split(file)[0]
    sub_dir=os.path.split(sub_dir)[1]
    out_dir2=os.path.join(out_dir,sub_dir)+"/"
    print(out_dir2)
    if not os.path.isdir(out_dir2):
        os.mkdir(out_dir2)
    shutil.copy2(file, out_dir2)