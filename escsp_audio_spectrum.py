###########################################################################
#Import Libraries section
import numpy as np 
# for visualizing the data 
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
# for opening the media file 
import scipy.io.wavfile as wavfile
#file handling and misc.
import os  
import subprocess
#import moviepy
from tracemalloc import stop
import glob
import datetime
###########################################################################
#Define Global Variables
#Path to data folder
data_folder="/Users/trae/Dropbox/programs/ESCSP_Data/"
frames_folder=os.path.join(data_folder,"frames/")
movie_folder=os.path.join(data_folder,"movies/")
raw_data_folder=os.path.join(data_folder,"raw_data/")
raw_data_folder='/Volumes/NPS_EclipseSoundScape_2017/AUDIO/CONG/'
#Number of seconds to trim data to
n_sec=10

#plot_title="Eclipse Data"
#plot_title="Elk Test"
#plot_title="Bison Test"
#plot_title="Eclipse Test"
#audio_filename="CONGE03903_TotalEclipse_20170818_171350.wav"
#audio_filename="CONGE03903_TotalEclipse_20170820_171350.wav"
#audio_filename="HumanCheeringInsects_ScottsBluff.wav"
#audio_filename="InsectAircraft_ScottsBluff.wav"
#audio_filename="InsectBird_GreatSmokey.wav"
#audio_filename="InsectBirdAircraft_Homestead.wav"
#audio_filename="Insects_GreatSmokey.wav"
#audio_filename="Wind_ScottsBluff.wav"
#audio_filename=".wav"
audio_filename="CONGE03903_20170821_160855.wav"
#movie_name="Eclipse test"
#movie_name="BisonYELL"
#movie_name="Elk_Test"
#Number of frames/sec
frames_per_second=24

audio_files=[os.path.join(raw_data_folder,audio_filename)]
for audio_file in audio_files:
    print(audio_file)
    base_filename, ext = os.path.splitext(os.path.basename(audio_file))

    movie_name1=os.path.join(movie_folder,base_filename+"_spectrogram_silent.mp4")
    movie_name2=os.path.join(movie_folder,base_filename+"_spectrogram.mp4")
    plot_title=base_filename
    audio_file_out=os.path.join(data_folder,"audi0_clip.wav")
#print(audio_file)
###########################################################################
#Remove any previous files.
    if os.path.isfile(movie_name1):
	    os.remove(movie_name1)
    if os.path.isfile(movie_name2):
	    os.remove(movie_name2)
    if os.path.isfile(audio_file_out):
	    os.remove(audio_file_out)
###########################################################################
# datetime(year, month, day, hour, minute, second, microsecond)
    clip_start_time=datetime.datetime(2017, 8,21,16,8,55)
    total_eclipse_start_time=datetime.datetime(2017,8,21, 18,42,33)
    total_eclipse_start_delta=(total_eclipse_start_time-clip_start_time).total_seconds()

    start_seconds=total_eclipse_start_delta-30.0
    end_seconds=total_eclipse_start_delta



#print(total_eclipse_start_delta)
#Audio Processing
#Fs=Sampling rate (Frequency, sample)
#aud = Audio data
    Fs, aud = wavfile.read(audio_file) 

    n_sec=int(len(aud[:,0])/Fs)
#n_sec=int(len(aud[Fs*135:,0])/Fs)
    aud_left = aud[:,0] # select left channel only

#first = aud_left[:int(Fs*n_sec)] # trim 
#first= aud_left[Fs*135:] # trim 
    first = aud_left
    wavfile.write(audio_file_out, Fs, first)
###########################################################################

    index=0

# Postion of plot one, the equalizer [left, bottom, width, height]
    ax1_position=[0.15, 0.79, 0.67, 0.16]
# Postion of plot two, the spectrogram [left, bottom, width, height]
    ax2_position=[0.15, 0.1, 0.85, 0.51]
    for iter_1 in range(n_sec):
        for iter_2 in range(frames_per_second):
            powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(first, Fs=Fs,
                xextent=[0,n_sec], mode="magnitude", scale="dB", cmap="inferno", scale_by_freq=False) 
            
            line_xs=[iter_1+(iter_2/frames_per_second),iter_1+(iter_2/frames_per_second)]
            line_ys=[min(frequenciesFound),max(frequenciesFound)]
        
            fig1 = plt.figure()
            ax = fig1.add_axes(ax1_position)
        
            #plt.subplot(2, 1, 1)
            #plt.axes([0., 0.3, 0.3, 0.3])    # [left, bottom, width, height]
            #ax = plt.gca()
            #ax.axes.xaxis.set_ticklabels([])
            #ax.set_ylim([np.min(powerSpectrum[:,index]), np.max(powerSpectrum[:,index])])
        
            #plt.yscale("log")  
            #ax.set_yticklabels([])
            #ax.set_xticklabels([])
        
            ax.set_yticks([])

            ax.set_xlabel('Frequency')
            ax.set_ylabel('Volume')
            ax.plot(frequenciesFound,powerSpectrum[:,index],color="#ff9300")
            ax.plot(frequenciesFound,-1.0*powerSpectrum[:,index],color="#ff9300")
            ax.fill_between(frequenciesFound,powerSpectrum[:,index],-1.0*powerSpectrum[:,index],color="#ff9300")
        
            ax2 = fig1.add_axes(ax2_position)# [left, bottom, width, height]
            powerSpectrum, frequenciesFound, time, imageAxis = ax2.specgram(first, Fs=Fs,
            xextent=[0,n_sec], mode="magnitude", scale="dB", cmap="inferno", scale_by_freq=False) 
        
            line_xs=[iter_1+(iter_2/frames_per_second),iter_1+(iter_2/frames_per_second)]
            line_ys=[min(frequenciesFound),max(frequenciesFound)]

       
            ax2.set_xlabel('Time (Seconds)')
            ax2.set_ylabel('Frequency')
        
            ax2.plot(line_xs,line_ys,'k')
        
            ax2.set_title('Spectrogram')
            plt.colorbar(imageAxis,label="Volume dB")
            frame_name="image_"+str(index).zfill(5)+".png"
                
            plt.savefig(os.path.join(frames_folder,frame_name))
            
            #Advance internal counter 1-step
            index+=1
        
            #Clear the plot's state
            plt.cla()
            plt.clf()

#
    print("Calling ffmpeg")
    print(movie_name1)
    frame="image_%5d.png"

    ffmpeg_call="/usr/local/bin/./ffmpeg -framerate "+str(frames_per_second)+" -i "+os.path.join(frames_folder, 
	    frame)+" "+movie_name1

    print(ffmpeg_call)
    process=subprocess.run(ffmpeg_call,shell=True)   

    #Add the clipped audio file to the movie file
    ffmpeg_call2="/usr/local/bin/./ffmpeg -i "+movie_name1+" -i "+audio_file_out+" -c:v copy -c:a aac "+movie_name2
    
    process=subprocess.run(ffmpeg_call2,shell=True) 

    if os.path.isfile(movie_name2):
	    print(movie_name2 + " has been created.") 

#final.write_videofile(movie_name)
    frames_list=glob.glob(os.path.join(frames_folder,"image_*.png"))
    for frame in frames_list:
        try:
            os.remove(frame)
        except:
            print("Error while deleting file : ", frame)