"""escsp_plot_eclipse_soundscapes.py
This is a program to plot the soundscape volume in a time during an eclipse with the same time on non-eclipse days providing error bars"""
###########################################################################
#Import Libraries section
import datetime
import glob
import os
###########################################################################
#Define Global Variables
#Path to data folder
data_folder="/Users/trae/Dropbox/programs/ESCSP_Data/"
frames_folder=os.path.join(data_folder,"frames/")
movie_folder=os.path.join(data_folder,"movies/")
plots_folder=os.path.join(data_folder,"plots/")

raw_data_folder="/Volumes/WD_04/NPS_EclipseSoundScape_2017/AUDIO/BICY/"

#Define the time that you want to plot out. This is usually determined by the time of the eclipse.
#Time to plot
plot_start_time=datetime.time(18,55,59)
#Day of Plot
plot_start_day=datetime.date(2017,8,25)
#Amount of time to plot in seconds
n_sec=45
n_sec_time_delta=datetime.timedelta(seconds=n_sec)



#Get the names of all of the files in the raw_data_folder
data_file_names=glob.glob(os.path.join(raw_data_folder,"*.wav"))
#print(data_file_names)
eclipse_time_file, other_days_at_time=


 

