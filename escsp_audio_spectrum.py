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
audio_filename="InsectBird_GreatSmokey.wav"
#audio_filename="InsectBirdAircraft_Homestead.wav"
#audio_filename="Insects_GreatSmokey.wav"
#audio_filename="Wind_ScottsBluff.wav"
#audio_filename=".wav"
audio_filename="nri-BisonYELL.wav"
#movie_name="Eclipse test"
#movie_name="BisonYELL"
#movie_name="Elk_Test"
#Number of frames/sec
frames_per_second=24

audio_file=os.path.join(raw_data_folder,audio_filename)
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
clip_start_time=datetime.datetime(2017, 8,21,17,13,50)
total_eclipse_start_time=datetime.datetime(2017, 8,21, 18,42,33)
total_eclipse_start_delta=(total_eclipse_start_time-clip_start_time).total_seconds()
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
x_temp=np.arange(0,2*np.pi, .1)
y_temp=np.sin(x_temp)
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
spacing = 0.005

index=0
for iter_1 in range(n_sec):
    for iter_2 in range(frames_per_second):
        powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(first, Fs=Fs,
         xextent=[0,n_sec], mode="magnitude", scale="dB", cmap="inferno", scale_by_freq=False) 
        line_xs=[iter_1+(iter_2/frames_per_second),iter_1+(iter_2/frames_per_second)]
        line_ys=[min(frequenciesFound),max(frequenciesFound)]
        
        plt.style.use('dark_background')

        plt.subplot(2, 1, 1)
        ax = plt.gca()
        #ax.axes.xaxis.set_ticklabels([])
        #ax.set_ylim([np.min(powerSpectrum[:,index]), np.max(powerSpectrum[:,index])])
        
        #plt.yscale("log")  
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])
        ax.set_yticks([])
        plt.xlabel('Frequency')
        plt.ylabel('Relative Volume')
        plt.plot(frequenciesFound,powerSpectrum[:,index],color="#ff9300")
        plt.plot(frequenciesFound,-1.0*powerSpectrum[:,index],color="#ff9300")
        ax.fill_between(frequenciesFound,powerSpectrum[:,index],-1.0*powerSpectrum[:,index],color="#ff9300")

        plt.subplot(2, 1, 2)
        powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(first, Fs=Fs,
         xextent=[0,n_sec], mode="magnitude", scale="dB", cmap="inferno", scale_by_freq=False) 
        line_xs=[iter_1+(iter_2/frames_per_second),iter_1+(iter_2/frames_per_second)]
        line_ys=[min(frequenciesFound),max(frequenciesFound)]
        plt.xlabel('Time (Seconds)')
        plt.ylabel('Frequency')
        #if  max(line_xs) > 0:
        #    plt.plot(line_xs,line_ys,'k')
        #plt.tight_layout()
        plt.plot(line_xs,line_ys,'k')
        #plt.plot([total_eclipse_start_delta, total_eclipse_start_delta], line_ys,'w')
        plt.colorbar(label="Volume dB")
        frame_name="image_"+str(index).zfill(5)+".png"
        #plt.suptitle(plot_title+" t="+str(iter_1).zfill(4)+" (s)")
        
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
#ffmpeg_call="/usr/local/bin/./ffmpeg -f image2 -r 12 -i  "+os.path.join(out_dir,
#ffmpeg_call="/usr/local/bin/./ffmpeg -f image2 -r 12 -i  "+os.path.join(frames_folder, 
#	 frame)+" -loglevel quiet -an -pix_fmt 'yuv420p' -vcodec 'libx264' -level 41 -crf 0.0 -b '28311k'\
#	 -r 12 -bufsize '28311k' -maxrate '28311k' -g '100' -coder 1 -profile main \
#	 -preset faster -qdiff 4 -qcomp 0.7 -directpred 3 -flags +loop+mv4 -cmp +chroma \
#	 -partitions +parti4x4+partp8x8+partb8x8 -subq 7 -me_range 16 -keyint_min 1 \
#	 -sc_threshold 40 -i_qfactor 0.71 -rc_eq 'blurCplx^(1-qComp)' -b_strategy 1 \
#	 -bidir_refine 1 -refs 6 -deblockalpha 0 -deblockbeta 0  -trellis 1 -x264opts\
#	  keyint=10:min-keyint=1:bframes=1 -threads 2 "+movie_name1

ffmpeg_call="/usr/local/bin/./ffmpeg -framerate "+str(frames_per_second)+" -i "+os.path.join(frames_folder, 
	 frame)+" "+movie_name1

print(ffmpeg_call)
process=subprocess.run(ffmpeg_call,shell=True)   

#Add the clipped audio file to the movie file
ffmpeg_call2="/usr/local/bin/./ffmpeg -i "+movie_name1+" -i "+audio_file_out+" -c:v copy -c:a aac "+movie_name2

process=subprocess.run(ffmpeg_call2,shell=True) 

if os.path.isfile(movie_name2):
	print(movie_name2 + " has been created.") 
#Add audio to the video
#audio_track = moviepy.editor.AudioFileClip(audio_file)
#video_track = moviepy.editor.VideoFileClip(movie_name)
#final = video_track.set_audio(audio_track)

#final.write_videofile(movie_name)
frames_list=glob.glob(os.path.join(frames_folder,"image_*.png"))
for frame in frames_list:
    try:
        os.remove(frame)
    except:
        print("Error while deleting file : ", frame)