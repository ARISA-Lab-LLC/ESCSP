#escsp_audio_change.py
###########################################################################
#Import Libraries section
import pickletools
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
from scipy.misc import derivative
import copy
###########################################################################
#Define Global Variables
#Path to data folder
data_folder="/Users/trae/Dropbox/programs/ESCSP_Data/"
frames_folder=os.path.join(data_folder,"frames/")
movie_folder=os.path.join(data_folder,"movies/")
raw_data_folder=os.path.join(data_folder,"raw_data/")
plots_folder=os.path.join(data_folder,"plots/")
#raw_data_folder='/Volumes/NPS_EclipseSoundScape_2017/AUDIO/FODO/'
#raw_data_folder='/Volumes/NPS_EclipseSoundScape_2017/AUDIO/HOME/'
#Start time in seconds
#start_seconds=int(8133)+45
#Number of seconds to trim data to
n_sec=45
speed_factor=int(1)
volume_factor=1
verbose=True
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
#audio_filename="People_and_Cars_Example_trimmed2.wav"
#audio_filename="Crickets-cicadas-and-grasshoppers.wav"
#audio_filename="People_and_Cars_Example_first_45.wav"
#audio_filename="Crickets-cicadas-and-grasshoppers_first_30.wav"
#audio_filename="CONGE03903_20170820_160856.wav"
#audio_filename="FODO_eclipse.wav"
#audio_filename="FODOE10882_20170821_160857.wav" # Test #1
audio_filename="BICYE03918_20170821_160855.wav" # Test #2
#movie_name="Eclipse test"
#movie_name="BisonYELL"
#movie_name="Elk_Test"
#Number of frames/sec
frames_per_second=16
if verbose:
    print(audio_filename)
    print(frames_per_second)


#    start_seconds=total_eclipse_start_delta-30.
#    end_seconds=total_eclipse_start_delta+0.
#    n_sec=int(end_seconds-start_seconds)
#    print("New file length: "+str(n_sec)+' seconds')
start_seconds=24.5*60.0
#end_seconds=start_seconds+n_sec
end_seconds=30.5*60.0
n_sec=end_seconds-start_seconds
audio_files=[os.path.join(raw_data_folder,audio_filename)]


for audio_file in audio_files:
    if verbose: print(audio_file)
    base_filename, ext = os.path.splitext(os.path.basename(audio_file))
    movie_base_name=base_filename+"_from_"+str(start_seconds).zfill(6)+"_to_"+str(end_seconds).zfill(6)
    movie_name1=os.path.join(movie_folder,movie_base_name+"_SCA_silent.mp4")
    movie_name2=os.path.join(movie_folder,movie_base_name+"_SCA.mp4")
    if verbose: print("Movie Name: "+movie_name2)
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
#Audio Processing
#Fs=Sampling rate (Frequency, sample)
#aud = Audio data
    if verbose: print("Opening wav file: ",audio_file)
    Fs_original, audio = wavfile.read(audio_file) 

    n_sec_recording=int(len(audio[:,0])/Fs_original)
    if verbose: print("Original file length: "+str(n_sec_recording)+' seconds')
#n_sec=int(len(audio[Fs*135:,0])/Fs)
    #audio_left = audio[:,0] # select left channel only
    #Combine left and right channels
    audio_mono=(audio[:,0]+audio[:,1])/2

# datetime(year, month, day, hour, minute, second, microsecond)
    #CONGE03903_20170821_193153.wav
#    clip_start_time=datetime.datetime(2017, 8,21,16,8,57)
#    total_eclipse_start_time=datetime.datetime(2017, 8,21,18,42,38)
#    total_eclipse_start_delta=(total_eclipse_start_time-clip_start_time).total_seconds()

    recording_time=int((n_sec)/speed_factor)
    
    Fs=int(Fs_original*speed_factor)   
    if verbose:
        print("Recording time: ",recording_time ) 
        print("Fs_original: ",Fs_original )
        print("Fs: ",Fs)
#print(total_eclipse_start_delta)
#trimmed_audio = audio_out[:int(Fs*n_sec)] # trim 
#trimmed_audio= audio_out[Fs*135:] # trim 
    audio_start_index=int(start_seconds*Fs_original)
    audio_end_index=int(end_seconds*Fs_original)
    trimmed_audio = audio_mono[audio_start_index:audio_end_index]
#Save some memory space
    del(audio_mono)

    trimmed_stereo=audio[audio_start_index:audio_end_index,:]#*volume_factor
#Save some memory space
    del(audio)
    wavfile.write(audio_file_out, Fs, trimmed_stereo)
#Save some memory space
    del(trimmed_stereo)

powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(trimmed_audio, Fs=Fs_original,
                xextent=[0,n_sec], mode="magnitude", scale="linear", cmap="inferno", 
                scale_by_freq=True) 

plt.cla()
plt.clf()
plt.close("all")

############################################
#Do calculations in linear units then switch to dB (10*log_10(linear_signal))
#integrate over the frequency axis
volume_linear=np.trapz(powerSpectrum, frequenciesFound, axis=0)
#Find the average in linear units
volume_average_linear=np.mean(volume_linear)
#Find the standard deviation in linear units
volume_std_linear=np.std(volume_linear)

#Calculate the volume in dB
volume_db=10*np.log10(volume_linear)
#Calculate the average volume in dB
volume_average_db=10*np.log10(volume_average_linear)
#Calculate the average volume + 1 std in dB
volume_average_plus_1std_db=10*np.log10(volume_average_linear+volume_std_linear)
#Calculate the average volume - 1 std in dB
temp_value=volume_average_linear-volume_std_linear
if temp_value<= 0: temp_value = 0.1
volume_average_minus_1std_db=10*np.log10(temp_value)
#Calculate the average volume + 2 std in dB
volume_average_plus_2std_db=10*np.log10(volume_average_linear+(2*volume_std_linear))
#Calculate the average volume - 2 std in dB
temp_value=volume_average_linear-(2*volume_std_linear)
if temp_value<= 0: temp_value = 0.1
volume_average_minus_2std_db=10*np.log10(temp_value)
#Calculate the average volume + 3 std in dB
volume_average_plus_3std_db=10*np.log10(volume_average_linear+(3*volume_std_linear))
#Calculate the average volume - 3 std in dB
temp_value=volume_average_linear-(volume_average_linear-(3*volume_std_linear))
if temp_value<= 0: temp_value = 0.1
volume_average_minus_3std_db=10*np.log10(temp_value)

zero_array=np.zeros(len(time))
#Make an array of the volume_average_db the same size as time for overplotting. 
volume_average_db_array=volume_average_db+zero_array
#Make an array of the volume_average_plus_2std_db the same size as time for overplotting. 
volume_average_plus_2std_db_array=volume_average_plus_2std_db+zero_array
#Make an array of the volume_average_minus_2std_db the same size as time for overplotting. 
volume_average_minus_2std_db_array=volume_average_minus_2std_db+zero_array

reduced_volume=volume_linear-np.average(volume_linear)
reduced_volume[np.where(reduced_volume < 0)]=0
deriv= np.gradient(reduced_volume)
avg_deriv=np.average(np.median(deriv))
positive_ind=np.where(deriv > 0)
negative_ind=np.where(deriv < 0)
reduced_deriv=copy.deepcopy(deriv)
reduced_deriv[positive_ind] -= avg_deriv
reduced_deriv[negative_ind] += avg_deriv

normal_deriv=deriv#/np.max(np.abs(deriv)))
normal_deriv=reduced_deriv/np.max(np.abs(reduced_deriv))
##############################################################################################
# Plotting section
# 
filename=os.path.join(plots_folder,movie_base_name+'_SCA.png')
plt.style.use('dark_background')
#ax=plt.gca()
#ax.set_xlabel('Time (Seconds)')
#ax.set_ylabel('Volume')
#ax.set_ylim([np.min(normal_deriv), np.max(normal_deriv)])
#ax.plot(time, normal_deriv, color='orange', label='Change')
plt.title('Soundscapes Computer Analysis')
plt.xlabel('Time (Seconds)')
plt.ylabel('Volume (Decibels)')
#plt.ylim([np.min(normal_deriv), np.max(normal_deriv)])
# formatting
# plt.legend(loc='upper left')
#plt.axes([0.3, 0.3, .5, .5])

plt.style.use('dark_background')
plt.grid(True)
#plot in log_10 scale
plt.yscale('linear')
plt.plot(time, volume_db, color='orange')

#Annotate with the average and std deviation underneath the plot.
plt.annotate(f"Average Volume: {volume_average_db:.2f} db",[0,-0.15],xycoords="axes fraction")
plt.annotate(f"Volume Standard Deviation Range: {volume_average_minus_2std_db:.2f} - {volume_average_plus_2std_db:.2f} db",[0,-0.2],xycoords="axes fraction")
plt.tight_layout()
#display plot (During testing only)
#plt.show() 

#save the plot to a png file
plt.savefig(filename)
#Save the plot to a file.
#plt.plot(time, normal_deriv, color='orange')
#Clear the plot's state
plt.cla()
plt.clf()
plt.close("all")

##############################################################################################
#
filename=os.path.join(plots_folder,movie_base_name+'_SCA_with_average.png')
plt.style.use('dark_background')
#ax=plt.gca()
#ax.set_xlabel('Time (Seconds)')
#ax.set_ylabel('Volume')
#ax.set_ylim([np.min(normal_deriv), np.max(normal_deriv)])
#ax.plot(time, normal_deriv, color='orange', label='Change')
plt.title('Soundscapes Computer Analysis')
plt.xlabel('Time (Seconds)')
plt.ylabel('Volume (Decibels)')
#plt.ylim([np.min(normal_deriv), np.max(normal_deriv)])
# formatting
# plt.legend(loc='upper left')
#plt.axes([0.3, 0.3, .5, .5])

plt.style.use('dark_background')
plt.grid(True)
#plot in log_10 scale
plt.yscale('linear')
plt.plot(time, volume_db, color='orange')
plt.plot(time, volume_average_db_array, color='green', linewidth=3)

#Annotate with the average and std deviation underneath the plot.
plt.annotate(f"Average Volume: {volume_average_db:.2f} db",[0,-0.15],xycoords="axes fraction")
plt.annotate(f"Volume Standard Deviation Range: {volume_average_minus_2std_db:.2f} - {volume_average_plus_2std_db:.2f} db",[0,-0.2],xycoords="axes fraction")
plt.tight_layout()
#display plot (During testing only)
#plt.show() 

#save the plot to a png file
plt.savefig(filename)
#Save the plot to a file.
#plt.plot(time, normal_deriv, color='orange')
#Clear the plot's state
plt.cla()
plt.clf()
plt.close("all")

##############################################################################################
#


filename=os.path.join(plots_folder,movie_base_name+'_SCA_with_average_std.png')
plt.style.use('dark_background')
#ax=plt.gca()
#ax.set_xlabel('Time (Seconds)')
#ax.set_ylabel('Volume')
#ax.set_ylim([np.min(normal_deriv), np.max(normal_deriv)])
#ax.plot(time, normal_deriv, color='orange', label='Change')
plt.title('Soundscapes Computer Analysis')
plt.xlabel('Time (Seconds)')
plt.ylabel('Volume (Decibels)')
#plt.ylim([np.min(normal_deriv), np.max(normal_deriv)])
# formatting
# plt.legend(loc='upper left')
#plt.axes([0.3, 0.3, .5, .5])

plt.style.use('dark_background')
plt.grid(True)
#plot in log_10 scale
plt.yscale('linear')
plt.plot(time, volume_db, color='orange')
plt.plot(time, volume_average_db_array, color='green', linewidth=3)
plt.plot(time, volume_average_plus_2std_db_array, color='blue', linewidth=3)
plt.plot(time, volume_average_minus_2std_db_array, color='blue', linewidth=3)

#Annotate with the average and std deviation underneath the plot.
plt.annotate(f"Average Volume: {volume_average_db:.2f} db",[0,-0.15],xycoords="axes fraction")
plt.annotate(f"Volume Standard Deviation Range: {volume_average_minus_2std_db:.2f} - {volume_average_plus_2std_db:.2f} db",[0,-0.2],xycoords="axes fraction")
plt.tight_layout()
#display plot (During testing only)
#plt.show() 

#save the plot to a png file
plt.savefig(filename)
#Save the plot to a file.
#plt.plot(time, normal_deriv, color='orange')
#Clear the plot's state
plt.cla()
plt.clf()
plt.close("all")
##############################################################################################
#Create movie.
index=0
for iter_1 in range(recording_time):
    "SCA=Soundscapes_Computer_Analysis"
    frame_base_name=os.path.join(frames_folder,base_filename+"_SCA_")
    for iter_2 in range(frames_per_second):
        plt.style.use('dark_background')
        plt.title('Soundscapes Computer Analysis')
        plt.xlabel('Time (Seconds)')
        plt.ylabel('Volume (Decibels)')
        plt.grid(True)
        plt.yscale('linear')
        plt.plot(time, volume_db, color='orange')

#Plot time bar overlay 
        bottom, top = plt.ylim()         
        line_x_position=iter_1+(iter_2/frames_per_second)
        line_xs=[line_x_position,line_x_position]
        line_ys=[bottom,top]
        plt.plot(line_xs,line_ys,'g')

#Annotate with the average and std deviation underneath the plot.
        plt.annotate(f"Average Volume: {volume_average_db:.2f} db",[0,-0.15],xycoords="axes fraction")
        plt.annotate(f"Volume Standard Deviation Range: {volume_average_minus_2std_db:.2f} - {volume_average_plus_2std_db:.2f} db",[0,-0.2],xycoords="axes fraction")
        plt.tight_layout()


#display plot (During testing only)
#plt.show() 

#save the plot to a png file
        frame_name="image_"+str(index).zfill(5)+".png"
        plt.savefig(os.path.join(frames_folder,frame_name))
#Advance internal counter 1-step
        index+=1
#Clear the plot's state
        plt.cla()
        plt.clf()
        plt.close("all")

#Combine frames to make a movie
del(trimmed_audio)
if verbose: print("Calling ffmpeg")
if verbose: print(movie_name1)
frame="image_%5d.png"

ffmpeg_call="/usr/local/bin/./ffmpeg -framerate "+str(frames_per_second)+" -i "+os.path.join(frames_folder, 
	frame)+" "+movie_name1

if verbose: print(ffmpeg_call)
process=subprocess.run(ffmpeg_call,shell=True)   

#Add the clipped audio file to the movie file
ffmpeg_call2="/usr/local/bin/./ffmpeg -i "+movie_name1+" -i "+audio_file_out+" -c:v copy -c:a aac "+movie_name2
    
process=subprocess.run(ffmpeg_call2,shell=True) 

if os.path.isfile(movie_name2):
    print(movie_name2 + " has been created.") 


#Remove frame files 
frames_list=glob.glob(os.path.join(frames_folder,"image_*.png"))
for frame in frames_list:
    try:
        os.remove(frame)
    except:
        print("Error while deleting file : ", frame)

