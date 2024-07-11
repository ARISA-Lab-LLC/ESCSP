from escsp import*
import os

indirs=[
    "/Volume/ESCSPF00/Total_Raw_Data/ESID#515/",
    "/Volume/ESCSPF00/Total_Raw_Data/ESID#516/",
    "/Volume/ESCSPF00/Total_Raw_Data/ESID#517/",
    "/Volume/SCSPF00/Total_Raw_Data/ESID#518/"
    ]
outdirs=[
    "/Volume/ESCSPF00/Total_Analysis_Data/ESID#515_TotalEclipse_AudioMothTimeChime_Split",
    "/Volume/ESCSPF00/Total_Analysis_Data/ESID#516_TotalEclipse_AudioMothTimeChime_Split",
    "/Volume/ESCSPF00/Total_Analysis_Data/ESID#517_TotalEclipse_AudioMothTimeChime_Split",
    "/Volume/ESCSPF00/Total_Analysis_Data/ESID#518_TotalEclipse_AudioMothTimeChime_Split"
    ]
format="%Y%m%d_%H%M%S"
for ii in range(len(indirs)):
    indir=indirs[ii]
    outdir=outdirs[ii]
    if os.path.isdir(indir):
        #split_wave_files(indir, outdir, verbose=True)
        files=glob.glob(os.path.join(folder,"*.WAV"))
        for file in files:
            print(file)
            dt=filename_2_datetime(files, type="AudioMoth", verbose=None)[0]
            print(dt.strftime(format))
            s2=
