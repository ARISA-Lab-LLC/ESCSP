#escsp_get_psd.py
"""Program to calculate the PSD of a group of WAV files."""

###########################################################################
#Import Libraries section
import pickletools
import numpy as np 
# for visualizing the data 
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
# for opening the media file 
import scipy.io.wavfile as wavfile
import scipy
#file handling and misc.
import os  
import subprocess
#import moviepy
from tracemalloc import stop
import glob
import datetime
from scipy.misc import derivative
import copy
from escsp import *
###########################################################################
#verbose = 1 

#Set the site folder
#folder="/Volumes/Austrian/Annular_DATA/ESID#003_AnnularEclipse_AudioMothTimeChime_Split/"
#plots_folder="/Volumes/Austrian/Dropbox/ARISA Lab/ES/ES_CSP/DATA/Plots"


def escsp_get_psd(folder, plots_folder, filelist=filelist, verbose=False):
    if verbose: print(folder)
    ESID=folder.split("#")[1][0:3]
    if verbose: print(ESID)
    plot_1_name=os.path.join(folder, "PSD_plot_"+ESID+".png")
    plot_1a_name=os.path.join(plots_folder, "PSD_plot_"+ESID+".png")
#set the eclipse start time
    eclipse_start_time = datetime.datetime(2023, 10, 14, 17, 34) 
#set the eclipse end time
    eclipse_end_time = datetime.datetime(2023, 10, 14, 17, 39)

    two_days_before_start_time=eclipse_start_time-datetime.timedelta(hours=48)
    two_days_before_end_time=eclipse_end_time-datetime.timedelta(hours=48)

    one_day_before_start_time=eclipse_start_time-datetime.timedelta(hours=24)   
    one_day_before_end_time=eclipse_end_time-datetime.timedelta(hours=24)

#Get all of the recording files at the site
    recording_files=glob.glob(os.path.join(folder,"*."+"WAV"))
    if verbose: print(len(recording_files))                         

    two_days_before_files=get_files_between_times(recording_files, two_days_before_start_time, two_days_before_end_time)
    one_day_before_files=get_files_between_times(recording_files, one_day_before_start_time, one_day_before_end_time)
    eclipse_files=get_files_between_times(recording_files, eclipse_start_time, eclipse_end_time)


    if eclipse_files: 
        eclipse_wav, fs_ecl=combine_wave_files(eclipse_files, filelist=filelist, verbose=verbose)
        #f0, eclipse_psd=scipy.signal.periodogram(eclipse_wav, fs_ecl)
        fig, ax =plt.subplots()
        ax.psd(eclipse_wav, Fs=fs_ecl, color="orange", label="Eclipse Day")

    if two_days_before_files :
        two_days_before_wav, fs_tdb = combine_wave_files(two_days_before_files, filelist=filelist, verbose=verbose)
        #f2, two_days_before_psd=scipy.signal.periodogram(two_days_before_wav, fs_tdb)
        ax.psd(two_days_before_wav, Fs=fs_tdb, color="green", label="Two Days Before")

    if one_day_before_files: 
        one_day_before_wav, fs_odb = combine_wave_files(one_day_before_files, filelist=filelist, verbose=verbose)
        #f1, one_day_before_psd=scipy.signal.periodogram(one_day_before_wav, fs_odb)
        ax.psd(one_day_before_wav, Fs=fs_odb, color="blue", label="One Day Before")


        legend = ax.legend(loc='upper center', shadow=True, fontsize='large')
        plt.savefig(plot_1_name)
        if verbose: print("Saved file "+plot_1_name)    
        plt.savefig(plot_1a_name)
        if verbose: print("Saved file "+plot_1a_name)
        plt.close(fig)


   # two_days_before_psd=scipy.signal.periodogram(two_days_before_wav, fs=fs_ecl, window='boxcar')#, 
                                             #nfft=None, detrend='constant', return_onesided=True, 
                                             #scaling='density', axis=-1)


    #one_day_before_psd=scipy.signal.periodogram(one_day_before_wav, fs=fs_ecl, window='boxcar')#, 
                                             #nfft=None, detrend='constant', return_onesided=True, 
                                             #scaling='density', axis=-1)


    #avg_std = np.mean( np.array([ old_set, new_set ]), axis=0 )
    #std = numpy.std((one_day_before_psd,two_days_before_psd), axis=0 )
 



