""" Ad hoc unit test program for escsp.py library
run escsp.py in ipython"""
import escsp
import os

#Path to data folder
data_folder="/Users/trae/Dropbox/programs/ESCSP_Data/"
frames_folder=os.path.join(data_folder,"frames/")
movie_folder=os.path.join(data_folder,"movies/")
raw_data_folder=os.path.join(data_folder,"raw_data/")
plots_folder=os.path.join(data_folder,"plots/")

audio_filename="BICYE03918_20170821_160855.wav" 

audio_files=[os.path.join(raw_data_folder,audio_filename)]
print(audio_files)
start_times, dates, site_names =escsp.get_audio_start_info(audio_files, verbose="on")

#Test the naming convention
