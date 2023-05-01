if __name__ == "__main__":
    print("Eclipse Soundscapes: Citizen Science Project Library")

"""escsp.py Library for the Eclipse Soundscapes: Citizen Science Project"""
###########################################################################
#Import Libraries section
import numpy as np 
# for visualizing the data 
# for opening the media file 
import scipy.io.wavfile as wavfile
#file handling and misc.
import os  
import datetime
###########################################################################

def get_audio_start_info(files, type="NPS", verbose=None):
    """ Return recording start information for a wave file based on the filename. 
    Start time and date returned using datetime format.
    NPS Files return: start_time, start_date, site_name """
    print("Here 1")
    for file in files:
        #Get the filename
        filename=os.path.basename(file)

        start_dates=[]
        start_times=[]
        site_names=[]

        if type == "NPS":
            filename=filename.split(".")[0]
            site_name, date_string, time_string=filename.split("_")

            start_date=datetime.date(int(date_string[0:4]),int(date_string[4:6]), int(date_string[6:8]))
            start_time=datetime.time(int(time_string[0:2]),int(time_string[2:4]),int(time_string[4:6]))

            if verbose != None:
                 print(start_date)
                 print(start_time)
            
            start_dates.append(start_date)
            start_times.append(start_time)
            site_names.append(site_name) 

            return start_times, start_dates, site_names

def get_wav_file_matching_datetime():
    """Get the filenames of wav file that matches the datetime entered and
    the filenames that match the time but on different days"""
    matching_file=""
    matching_file_on_other_days=""
    return matching_file, matching_file_on_other_days

def



