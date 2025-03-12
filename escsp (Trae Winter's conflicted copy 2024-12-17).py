if __name__ == "__main__":
    print("Eclipse Soundscapes: Citizen Science Project Library")

"""escsp.py Library for the Eclipse Soundscapes: Citizen Science Project"""
###########################################################################
#Import Libraries section
import numpy as np 
# for visualizing the data 
# for opening the media file 
import scipy.io.wavfile as wavfile
from scipy.misc import derivative
import scipy
import wave
#file handling and misc.
import os 
import shutil 
import datetime
import pytz
import pandas as pd
from natsort import natsorted
import glob
# for visualizing the data 
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
import subprocess
#import moviepy
from tracemalloc import stop
import copy
from moviepy.editor import *
import re
###########################################################################
#Global Variables
user_images=None
youtube_assets_folder="./YouTube_Assets/"
#privacyStatus="private"
privacyStatus="public"
AM_Spreadsheet=os.getenv("total_redacted_AM_spreadsheet")
###########################################################################

def mk_eclipse_data_csv(folder):
    if os.path.isdir(folder):
         AM_df=pd.read_csv(AM_Spreadsheet)
         ESID=filename_2_ESID(folder)
         row = AM_df[AM_df['AudioMoth ES ID Number'] == ESID]
         eclipse_data=row[['AudioMoth ES ID Number', 
                           "Latitude",
                           "Longitude",
                           "Eclipse Type",
                           "Total Eclipse Start UTC", 
                           "Total Eclipse End UTC",
                           "Max Eclipse Time UTC", 
              "Upload Round",
              "Unusable Data 1 = Unusable",
              "Manually Add ES ID# to Raw Data Upload 1 = Need to Do",
              "Audio Data YouTube Link", 
              "Not filtered (All frequencies), 4/6/2024 PSD",
              "Not filtered (All frequencies), 4/7/2024 PSD",
              "Not filtered (All frequencies), Average PSD of 4/6 & 4/7",
              "Not filtered (All frequencies), 4/8/2024 PSD",
              "Not filtered (All frequencies), Standard Deviation (Average vs Eclipse)",
              "Filtered (Cricket frequency), 4/6/2024 PSD",
              "Filtered (Cricket frequency), 4/7/2024 PSD",
              "Filtered (Cricket frequency), Average PSD of 4/6 & 4/7",
              "Filtered (Cricket frequency), eclipse 4/8/2024 PSD",
              "Filtered (Cricket frequency), Standard Deviation (Average vs Eclipse)"
                           
                           ]].copy()



         
         
    else: 
         print("mk_eclipse_data_csv")
         print(folder+" is not a folder")
     
def get_audio_start_info(files, file_type="AudioMoth", verbose=None):
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

        if file_type == "NPS":
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
        
        if file_type == "AudioMoth":
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

def read_am_config(config_file):
    """ 
    Read an AudioMoth CONFIG.TXT file.
    
    Parameters:
    config_file: Path to an AudioMoth CONFIG.TXT file.
    
    Returns:
    result_dict: A dictionary of key value pairs generated from the CONFIG.TXT file.

    Example usage:
    directory_path = 'your_directory_path'
    all_files = list_files_in_directory(directory_path)
    """

    result_dict = {}
    
    with open(config_file, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if ':' in line:
                key, value = line.split(':', 1)  # Split only on the first colon
                result_dict.update({key.strip() : value.strip()})  # Remove leading/trailing whitespace from key and value
    
    return result_dict

def read_escsp_setup():
    """read the escsp_setup.cdat csv file that sets filepaths"""

    return escsp_info

def escsp_read_eclipse_csv(eclipse_data_csv, verbose=None):
    """
    Calculate the standard deviation of three functions given x and y values for each. 
     
     Args: 
        - eclipse_data_csv (string): Path to eclipse_data.csv file. 
        - old (anything): Old version of the eclipse_data.csv file was 'list type'. The new version is 'dict like'. 

     Returns: - dictionary of values: 
    """
    eclipse_info=None
    if os.path.isfile(eclipse_data_csv) :
        df=pd.read_csv(eclipse_data_csv, header=[0])
        column_names=list(df)

        #If the data frame is 'list type' do the following.  
        if 'ESID' not in column_names: 
            
            time_format="%Y-%m-%d %H:%M:%S"
            if verbose: print("success! " + eclipse_data_csv) 
            eclipse_info={"ESID": df.iloc[0, 1], 
                  "Latitude":df.iloc[1, 1], 
                  "Longitude" :df.iloc[2, 1],
                  "Eclipse_type" :df.iloc[3, 1], 
                  "CoveragePercent" :df.iloc[4, 1], 
                  "FirstContactDate" :df.iloc[5, 1], 
                  "FirstContactTimeUTC" :df.iloc[6, 1], 
                  "SecondContactTimeUTC" :df.iloc[7, 1], 
                  "ThirdContactTimeUTC" :df.iloc[8, 1], 
                  "FourthContactTimeUTC" :df.iloc[9, 1], 
                  "MaxEclipseTimeUTC" :df.iloc[10, 1] }
            
        #
        else: 
            if 'LocalType' in df.columns:
                 df.rename(columns={'LocalType': 'Eclipse_type'}, inplace=True)
            if 'TotalEclipseTimeUTC' in df.columns:
                 df.rename(columns={'TotalEclipseTimeUTC': 'MaxEclipseTimeUTC'}, inplace=True)
            
            eclipse_info=df.to_dict(orient='records')
            eclipse_info=eclipse_info[0]
        

    else: print('Error! No file named '+eclipse_data_csv)

    return eclipse_info

def escsp_get_eclipse_time_trio(eclipse_info, verbose=True):
    time_format="%Y-%m-%d %H:%M:%S"
    eclipse_type=eclipse_info["Eclipse_type"]
    if eclipse_type == "Annular" or eclipse_type == "Total":
        second_contact=eclipse_info["FirstContactDate"] + " " +eclipse_info["SecondContactTimeUTC"] 
        if verbose: print("eclipse_type: " + eclipse_type)
         
        if verbose: print("Second contact: "+second_contact)
        eclipse_start_time = datetime.datetime.strptime(second_contact, time_format) 
#set the eclipse end time
        third_contact = eclipse_info["FirstContactDate"] + " " +eclipse_info["ThirdContactTimeUTC"] 
        if verbose: print("Third contact: "+third_contact)
        eclipse_end_time =  datetime.datetime.strptime(third_contact, time_format) 

    else: #Set the range to be 3 minutes before and after the eclipse.
        if verbose: 
             print(type(eclipse_info['ESID']))
             print(eclipse_info['ESID'])
             print(type(eclipse_info["FirstContactDate"]))
        max_eclipse= eclipse_info["FirstContactDate"] + " " +eclipse_info["MaxEclipseTimeUTC"] 
        max_eclipse_time=datetime.datetime.strptime(max_eclipse, time_format)
        eclipse_start_time=max_eclipse_time-datetime.timedelta(minutes=3)
        eclipse_end_time=max_eclipse_time+datetime.timedelta(minutes=3)

    two_days_before_start_time=eclipse_start_time-datetime.timedelta(hours=48)
    two_days_before_end_time=eclipse_end_time-datetime.timedelta(hours=48)

    one_day_before_start_time=eclipse_start_time-datetime.timedelta(hours=24)   
    one_day_before_end_time=eclipse_end_time-datetime.timedelta(hours=24)
    
    eclipse_time_trio={
        "eclipse_start_time":eclipse_start_time,
        "eclipse_end_time":eclipse_end_time,
        "two_days_before_start_time":two_days_before_start_time,
        "two_days_before_end_time":two_days_before_end_time,
        "one_day_before_start_time":one_day_before_start_time,
        "one_day_before_end_time":one_day_before_end_time
        }
    
    return eclipse_time_trio
    
def filename_2_datetime(files, file_type="AudioMoth", verbose=False):
    """ Return a list if datetimes that correspond to the name of a WAV file"""
    if verbose : print("Here 1")
    if type(files) == type('a'): files=[files]
    date_times=None

    date_times=[]
    for count, file in enumerate(files):
         if not file.strip(): 
              print("blank file")
              files.pop(count)

    for file in files:
        #Get the filename
        if verbose : print('file= '+file)
        filename=os.path.basename(file).split(".")[0]
        if verbose : print('filename= '+filename)

        if file_type == "NPS": date_times=None

        if file_type == "AudioMoth":
            if verbose : print("--")
            if verbose : print(filename)
            if verbose : print(filename.split("_"))
            if verbose : print('*')
            if True: #try
                    
                date_string, time_string=filename.split("_")
                if verbose : print('date_string= '+date_string)
                if verbose : print('time_string= '+time_string)

                #start_date=datetime.date(int(date_string[0:4]),int(date_string[4:6]), int(date_string[6:8]))
                #start_time=datetime.time(int(time_string[0:2]),int(time_string[2:4]),int(time_string[4:6]))

                year=int(date_string[0:4])
                month=int(date_string[4:6])
                day=int(date_string[6:8])

                hour=int(time_string[0:2])
                minute=int(time_string[2:4])
                second=int(time_string[4:6])

                dandt=datetime.datetime(year, month, day, hour, minute, second)
                date_times.append(dandt)

            else: #except
                print("Unusable file skipped: "+file+" (filename_2_datetime)")
                    
    return date_times

def get_files_between_times(files, start_time, end_time):
    """Return only the filepaths for the recording files that are between the start_time & the end_time"""

    #I know there is a better way (more matrix) to do this, but I don't have the time to figure it out.
    return_files=None
    for file in files:
        date_and_time=filename_2_datetime(file, file_type="AudioMoth")
        date_and_time=date_and_time[0]
        if date_and_time >= start_time and date_and_time <= end_time: 
            if not return_files: return_files=[file]
            else: return_files.append(file)

    return return_files

def combine_wave_files(files, verbose=None):
    """Open the wave files in the list 'files' and combine them into one long wave file"""
    
    audio=False
    Fs_original=False

    counter=0
    if verbose: print("Number of files= "+str(len(files)))
    for file in files:
        if verbose: print("File for combine files= "+file)
        if counter == 0: Fs_original, audio = wavfile.read(file) 
        else: 
             Fs_2, audio_2 = wavfile.read(file) 
             if Fs_2 != Fs_original: print("Error in combine_wave_files.  Sample sizes are not the same. File= "+file)
             audio=np.concatenate((audio, audio_2), axis=0) # scipy.sparse.vstack(audio, audio_2)

        counter+=1

    return audio, Fs_original

def convert_to_utc(time_str, timezone_str, time_format="%Y-%m-%d %H:%M:%S"):
    """
    Convert a time from a specified timezone to UTC.

    Args:
    - time_str (str): The time string to convert.
    - timezone_str (str): The timezone of the input time string (e.g., 'America/New_York').
        'America/New_York',
        'US/Alaska'
        'US/Aleutian'
        'US/Arizona'
        'US/Central'
        'US/East-Indiana'
        'US/Eastern'
        'US/Hawaii'
        'US/Indiana-Starke'
        'US/Michigan'
        'US/Mountain'
        'US/Pacific'
        'US/Samoa' 
    - time_format (str): The format of the input time string. Default is "%Y-%m-%d %H:%M:%S".

    Returns:
    - str: The converted time in UTC as a string in the same format as the input.
    """
    # Create a timezone object for the specified timezone
    local_timezone = pytz.timezone(timezone_str)

    # Parse the input time string into a naive datetime object
    naive_datetime = datetime.datetime.strptime(time_str, time_format)

    # Localize the naive datetime to the specified timezone
    localized_datetime = local_timezone.localize(naive_datetime)

    # Convert the localized datetime to UTC
    utc_datetime = localized_datetime.astimezone(pytz.utc)

    # Return the UTC time
    return utc_datetime

def adjust_am_datetime(files, start_time, timezone_str, time_format_in="%Y-%m-%d %H:%M:%S", move=True, verbose=False):
    """Program to adjust the time of AudioMoth files if the time was not properly set. 
      Requires a set of recording files and a datetime object of the reported start time.

    Args:
    -files (list): List of strings containg the paths to the files.  
    -
    - timezone_str (str): The timezone of the input time string (e.g., 'America/New_York').
        'US/Alaska'
        'US/Aleutian'
        'US/Arizona'
        'US/Central'
        'US/East-Indiana'
        'US/Eastern'
        'US/Hawaii'
        'US/Indiana-Starke'
        'US/Michigan'
        'US/Mountain'
        'US/Pacific'
        'US/Samoa' 
        
    """
    files=natsorted(files)
    new_filenames=[]
    delta_time=None
    counter=0

    time_format="%Y%m%d_%H%M%S"
    if verbose: 
         start_time_dt=datetime.datetime.strftime(start_time, format=time_format)
         print("AudioMoth Reported time: "+start_time_dt.strptime(time_format))
    start_time_utc=convert_to_utc(start_time, timezone_str, time_format=time_format_in)
    if verbose: print("UTC Timestamp: "+start_time_utc.strptime(time_format))
    for file in files:  
        if verbose: print("File= "+ file)
        d_and_t_0=filename_2_datetime(file, file_type="AudioMoth")
        #Convertd_and_t_0 to an offset-aware datetime
        #Create a timezone object for the specified timezone
        utc_timezone = pytz.timezone('UTC')
        # Localize the naive datetime to the specified timezone
        d_and_t_0 = utc_timezone.localize(d_and_t_0[0])

        if counter== 0:
            if verbose: print("Calculating ")
            delta_time=start_time_utc-d_and_t_0
            if verbose: print("Time delta is "+str(delta_time))
        
        new_time=d_and_t_0+delta_time
        counter+=1
        new_file=file.split(os.path.basename(file))[0]+new_time.strftime(time_format)+".WAV"
        new_filenames.append(new_file)
        if move:
             shutil.move(file, new_file)

         
    #print(delta_times)

    return new_filenames #updated_file_names

def get_es_folder_list(top_level, verbose=False, split = False):
    """ Program to get all of the ES sub-folders from a top level directory."""
    subfolders = [ f.path for f in os.scandir(top_level) if f.is_dir() ]

    if split:
        subfolders2=[]
        for folder in subfolders:
            if folder.split("_")[len( folder.split("_"))-1] == 'Split':
                subfolders2.append(folder)

        if len(subfolders2) >= 1 : subfolders=subfolders2

    if verbose: print(subfolders)
    return subfolders
                    
def filename_2_ESID(file, verbose=False):

    """
    Extracts the three digits following the pattern 'ESID#' in the provided text.
    If there is an "A" after the the 3 digits then an "A" is added
    
    Args:
    - text (str): The input string containing the 'ESID#' pattern.
    
    Keyword arguments:
    -verbose (any): If set with anything other than None or False, print statements
        will be executed.

    Returns:
    - str: The ESID# (in 3 or 4 characters) if found, else None.
    """

    esid=None
    # Regular expression to find three digits following 'ESID#'
    match = re.search(r"ESID#(\d{3})", file)
    if match:
        esid=match.group(1)
        if esid+"A" in file: esid=esid+"A"
        if esid+"B" in file: esid=esid+"B"
        if esid+"a" in file: esid=esid+"a"
        if esid+"b" in file: esid=esid+"b"
        if verbose: print(f"Extracted ESID digits: {esid}")
    

    if esid ==None:
         if verbose: print("No ESID digits found.")
             
   
    return esid

def average_functions(x1, y1, x2, y2):
    """
    Calculate the average of two functions given x and y values for each.
    
    Args:
    - x1, y1 (array-like): The x and y values of the first function.
    - x2, y2 (array-like): The x and y values of the second function.
    
    Returns:
    - (numpy.ndarray, numpy.ndarray): The x values and the averaged y values.
    """
    # Ensure the input arrays are numpy arrays
    x1 = np.array(x1)
    y1 = np.array(y1)
    x2 = np.array(x2)
    y2 = np.array(y2)
    
    # Find common x values (this can be adjusted depending on the application)
    x_common = np.union1d(x1, x2)
    
    # Interpolate y values to the common x values
    interp_y1 = scipy.interpolate.interp1d(x1, y1, kind='linear', fill_value='extrapolate')
    interp_y2 = scipy.interpolate.interp1d(x2, y2, kind='linear', fill_value='extrapolate')
    
    y1_common = interp_y1(x_common)
    y2_common = interp_y2(x_common)
    
    # Compute the element-wise average
    avg_y_common = (y1_common + y2_common) / 2
    
    return x_common, avg_y_common

def standard_deviation_of_3_functions(x1, y1, x2, y2, x3, y3): 
     """ Calculate the standard deviation of three functions given x and y values for each. 
     Args: 
        - x1, y1 (array-like): The x and y values of the first function. 
        - x2, y2 (array-like): The x and y values of the second function. 
        - x3, y3 (array-like): The x and y values of the third function. 
     
     Returns: - (numpy.ndarray, numpy.ndarray): 
     The common x values and the standard deviation of the y values at each common x value. 
     """ 
     
     # Ensure the input arrays are numpy arrays 
     x1 = np.array(x1) 
     y1 = np.array(y1) 
     x2 = np.array(x2) 
     y2 = np.array(y2) 
     x3 = np.array(x3) 
     y3 = np.array(y3) 
     # Find common x values (this can be adjusted depending on the application) 
     x_common = np.union1d(np.union1d(x1, x2), x3) 
     # Interpolate y values to the common x values 
     interp_y1 = scipy.interpolate.interp1d(x1, y1, kind='linear', fill_value='extrapolate') 
     interp_y2 = scipy.interpolate.interp1d(x2, y2, kind='linear', fill_value='extrapolate') 
     interp_y3 = scipy.interpolate.interp1d(x3, y3, kind='linear', fill_value='extrapolate') 
     y1_common = interp_y1(x_common) 
     y2_common = interp_y2(x_common) 
     y3_common = interp_y3(x_common) 
     # Stack the y values to form a 2D array where each row corresponds to an x value 
     y_values = np.vstack((y1_common, y2_common, y3_common)) 
     # Compute the standard deviation across the rows (for each x value) 
     std_y_common = np.std(y_values, axis=0) 
     
     return x_common, std_y_common

def standard_deviation_of_2_functions(x1, y1, x2, y2): 
     """ Calculate the standard deviation of three functions given x and y values for each. 
     
     Args: 
        - x1, y1 (array-like): The x and y values of the first function. 
        - x2, y2 (array-like): The x and y values of the second function. 

     Returns: - (numpy.ndarray, numpy.ndarray): 
     The common x values and the standard deviation of the y values at each common x value. """ 
     # Ensure the input arrays are numpy arrays 
     x1 = np.array(x1) 
     y1 = np.array(y1) 
     x2 = np.array(x2) 
     y2 = np.array(y2) 
     # Find common x values (this can be adjusted depending on the application) 
     x_common = np.union1d(x1, x2)
     # Interpolate y values to the common x values 
     interp_y1 = scipy.interpolate.interp1d(x1, y1, kind='linear', fill_value='extrapolate') 
     interp_y2 = scipy.interpolate.interp1d(x2, y2, kind='linear', fill_value='extrapolate') 
     y1_common = interp_y1(x_common) 
     y2_common = interp_y2(x_common) 
     # Stack the y values to form a 2D array where each row corresponds to an x value 
     y_values = np.vstack((y1_common, y2_common)) 
     # Compute the standard deviation across the rows (for each x value) 
     std_y_common = np.std(y_values, axis=0) 
     
     return x_common, std_y_common

def escsp_get_psd(folder, plots_folder, filelist=None, eclipse_type = "Total", verbose=False):
    if verbose: print(folder)
    ESID=filename_2_ESID(folder)
    if verbose: print("ESID #=" + ESID)
    plot_1_name=os.path.join(folder, "PSD_plot_"+ESID+".png")
    if verbose: print("plot_1_name= "+plot_1_name)
    plot_1a_name=os.path.join(plots_folder, "PSD_plot_"+ESID+".png")
    eclipse_data_csv=os.path.join(folder, "eclipse_data.csv")
    day_one=False
    day_two=False
    day_eclipse=False
    if os.path.isfile(eclipse_data_csv) :
        df=pd.read_csv(eclipse_data_csv, header=[0])
        time_format="%Y-%m-%d %H:%M:%S"
        if verbose: print("success! " + eclipse_data_csv) 
        if eclipse_type == "Annular" or eclipse_type == "Total":
#set the eclipse start time
            chars_to_remove=["\"", "\'", "[", "]"]
            second_contact=str(df["FirstContactDate"].values[0]+" "+df["SecondContactTimeUTC"].values[0])
            for char_to_remove in chars_to_remove:
                second_contact.replace(char_to_remove, '')
            print(second_contact)
        #eclipse_start_time = datetime.datetime(2023, 10, 14, 17, 34) 
            eclipse_start_time = datetime.datetime.strptime(second_contact, time_format) 
#set the eclipse end time
        #eclipse_end_time = datetime.datetime(2023, 10, 14, 17, 39)
            third_contact = str(df["FirstContactDate"].values[0]+" "+df["ThirdContactTimeUTC"].values[0])
            for char_to_remove in chars_to_remove:
                third_contact.replace(char_to_remove, '')
            eclipse_end_time =  datetime.datetime.strptime(third_contact, time_format) 
        else:
            max_eclipse=datetime.datetime.strptime(
                df["FirstContactDate"].values[0]+ " " + df["TotalEclipseTimeUTC"].values[0], time_format)
            eclipse_start_time=max_eclipse-datetime.timedelta(minutes=3)
            eclipse_end_time=max_eclipse+datetime.timedelta(minutes=3)

        two_days_before_start_time=eclipse_start_time-datetime.timedelta(hours=48)
        two_days_before_end_time=eclipse_end_time-datetime.timedelta(hours=48)

        one_day_before_start_time=eclipse_start_time-datetime.timedelta(hours=24)   
        one_day_before_end_time=eclipse_end_time-datetime.timedelta(hours=24)

#Get all of the recording files at the site
        recording_files=glob.glob(os.path.join(folder,"*."+"WAV"))
        if verbose: print(len(recording_files))   

        
        eclipse_files=None
        two_days_before_files=None
        one_day_before_files=None                      

        two_days_before_files=get_files_between_times(recording_files, two_days_before_start_time, two_days_before_end_time)     
        one_day_before_files=get_files_between_times(recording_files, one_day_before_start_time, one_day_before_end_time)
        eclipse_files=get_files_between_times(recording_files, eclipse_start_time, eclipse_end_time)


#If the filelist parameter is set, then write the names of the files to the filelst file.  
        if filelist:
            if os.path.isfile(filelist):
                list_file=filelist
            else:
                list_file=os.path.join(folder, ESID+'_Analysis_Files.csv')
            
            if eclipse_files:
                df_=pd.DataFrame({'Eclipse Files': eclipse_files}) 
                if two_days_before_files:
                    df.insert(1, 'Two Days Before Files', two_days_before_files, True)
                else: df=pd.DataFrame({'Two Days Before Files': ["None"]}) 
                if one_day_before_files:
                    df.insert(1, 'One Day Before Files', one_day_before_files, True)
                else: df=pd.DataFrame({'One Day Before Files': ["None"]})       

            else: 
                df=pd.DataFrame({'Eclipse Files': ["None"]})    
            
            df.to_csv(list_file, index=False)

        if eclipse_files: 
            day_eclipse=True
            eclipse_wav, fs_ecl=combine_wave_files(eclipse_files, verbose=verbose)
            #f0, eclipse_psd=scipy.signal.periodogram(eclipse_wav, fs_ecl)
            fig, ax =plt.subplots()
            ax.psd(eclipse_wav, Fs=fs_ecl, color="orange", label="Eclipse Day")

        if two_days_before_files :
            day_two=True
            print("Length of filelist: " + str(len(two_days_before_files)))
            two_days_before_wav, fs_tdb = combine_wave_files(two_days_before_files, verbose=verbose)
            #f2, two_days_before_psd=scipy.signal.periodogram(two_days_before_wav, fs_tdb)
            ax.psd(two_days_before_wav, Fs=fs_tdb, color="green", label="Two Days Before")

        if one_day_before_files: 
            day_one=True
            one_day_before_wav, fs_odb = combine_wave_files(one_day_before_files, verbose=verbose)
            #f1, one_day_before_psd=scipy.signal.periodogram(one_day_before_wav, fs_odb)
            ax.psd(one_day_before_wav, Fs=fs_odb, color="blue", label="One Day Before")


            legend = ax.legend(loc='upper center', shadow=True, fontsize='large')
            plt.savefig(plot_1_name)
            if verbose: print("Saved file "+plot_1_name)    
            plt.savefig(plot_1a_name)
            if verbose: print("Saved file "+plot_1a_name)
            plt.close(fig)

        if day_one and day_two and day_eclipse:
             freqs_ecl, Pxx_den_ecl = scipy.signal.welch(eclipse_wav, fs_ecl)
             freqs_two_days_before, Pxx_den_two_days_before = scipy.signal.welch(two_days_before_wav, fs_tdb)
             freqs_one_day_before_wav, Pxx_den_one_day_before = scipy.signal.welch(one_day_before_wav, fs_ecl)

             common_freqs1, baseline=average_functions(freqs_one_day_before_wav, Pxx_den_one_day_before, freqs_two_days_before, freqs_two_days_before)

             common_freqs2, relative_psd=average_functions(freqs_ecl,Pxx_den_ecl,common_freqs1,  baseline)
             
             x_common, std_y_common=standard_deviation_of_3_functions(freqs_one_day_before_wav, Pxx_den_one_day_before,
                                                                    freqs_two_days_before, Pxx_den_two_days_before, 
                                                                    freqs_ecl, freqs_ecl)
             
             base_x_common, base_std_y_common=standard_deviation_of_2_functions(common_freqs1, baseline, freqs_ecl, freqs_ecl)
        
        print(df["ESID#"], np.max(base_std_y_common/np.mean(base_std_y_common)))
        print(np.max(relative_psd))




    else:
        print("No file "+eclipse_data_csv+" found.")

def escsp_mk_youtube_description(eclipse_info, Recording_Date,Recording_Start_Time,
                                 Recording_type, Photo_Credit,Photo_Description):
    if eclipse_info["FirstContactDate"] == "2023-10-14":
        file1=os.path.join(youtube_assets_folder,"annular_youtube_text_00.txt")
        file2=os.path.join(youtube_assets_folder,"annular_youtube_text_02.txt")
    else:
        file1=os.path.join(youtube_assets_folder,"total_youtube_text_00.txt")
        file2=os.path.join(youtube_assets_folder,"total_youtube_text_02.txt")

    f1=open(file1, "r")
    f2=open(file2, "r")

    text1=f1.read()
    text2=f2.read()

    f1.close()
    f2.close()

    text=text1
    text=text+"Recording Date: "+Recording_Date+"\n"
    text=text+"Recording Start Time: "+Recording_Start_Time+"\n"
    text=text+"Latitude: "+ eclipse_info["Latitude"] +"\n"
    text=text+"Longitude: "+ eclipse_info["Longitude"]  +"\n"
    text=text+"Type of Eclipse: " + Recording_type +"\n\n"
    text=text+text2
    text=text+"\n\n"
    text=text+"Photo Credit: " +Photo_Credit+ "\n"
    text=text+"Photo Description: " +Photo_Description+ "\n"

    return text
    
def get_eclipse_images(ESID, eclipse_type=None, user_images=None, verbose=False):
        if verbose: print("eclipse_type= "+eclipse_type)
        eclipse_image_file=None
        Photo_Credit=None
        Photo_Description=None 
        eclipse_images=[os.path.join(youtube_assets_folder,"Annular_Eclipse_YouTube_Image.jpg"),
                            os.path.join(youtube_assets_folder,"Partial_Eclipse_YouTube_Image.jpg"),
                            os.path.join(youtube_assets_folder,"Non-eclipse_days_YouTube_Image_Outdoor_Tree_Picture.jpg"),
                            os.path.join(youtube_assets_folder,"Total_Eclipse_image_YouTube.jpg")]
            
        if eclipse_type != None:
            if eclipse_type == "Annular" : 
                eclipse_image_file=eclipse_images[0]
                Photo_Credit="Shutterstock: Stock Photo ID: 1598297254, Contributor Hyserb"
                Photo_Description="Annular Solar Eclipse of the Sun in Hofuf, Saudi Arabia.  "
                Photo_Description=Photo_Description+"Annular solar eclipse over a hazy desert landscape, "
                Photo_Description=Photo_Description+"with a bright ring of the sun visible around the moon. "
                Photo_Description=Photo_Description+"The sky glows in a deep orange hue, enhancing the mystical appearance of the scene."

            if eclipse_type == "Partial" : 
                eclipse_image_file=eclipse_images[1]
                Photo_Credit="Credit: Evan Zucker"
                Photo_Description="Silhouette of wind turbines on the horizon during a sunset, "
                Photo_Description=Photo_Description+"with a dramatic crescent solar eclipse visible in the background, "
                Photo_Description=Photo_Description+"casting a warm orange glow in the sky."


            if eclipse_type == "Non-Eclipse" or eclipse_type == "Non-Eclipse-Day" : 
                eclipse_image_file=eclipse_images[2]
                Photo_Credit="Shutterstock"
                Photo_Description="Green leaves covering the top of several trees, with "
                Photo_Description=Photo_Description+"sunlight shining through and making spots of light on the ground below."

            if eclipse_type == "Total" : 
                eclipse_image_file=eclipse_images[3]
                Photo_Credit="Evan Zucker"
                Photo_Description="Blank for now"

        if not eclipse_image_file: 
            eclipse_image_file=eclipse_images[2]
            Photo_Credit="Shutterstock"
            Photo_Description=" Blank for now"

        return eclipse_image_file, Photo_Credit, Photo_Description

def escsp_mk_youtube_csv(you_tube_filename, clip_title, description, clip_basename, eclipse_info, youtube_folder):

    keywords="solar eclipse, soundscapes, Eclipse Soundscapes, citizen science, NASA, "+eclipse_info["Eclipse_type"]+" eclipse"
    youtube_dict={"file":[you_tube_filename],
                  "title":[clip_title], 
                  "description":[description],
                  "keywords":[keywords],
                  "category":["14"],
                  privacyStatus:[privacyStatus]}
    df=pd.DataFrame.from_dict(youtube_dict)
    df.to_csv(os.path.join(youtube_folder,clip_basename+"_youtube.csv"), index=False)

def escsp_mk_video_clip(audio_filename=None, eclipse_image_file=None,
                        video_filename=None,verbose=False):
    if verbose:
         print("audio_filename: "+audio_filename)
         print("eclipse_image_file: "+eclipse_image_file)
         print("video_filename: "+video_filename)

    # Import the audio(Insert to location of your audio instead of audioClip.mp3)
    audio = AudioFileClip(audio_filename)
    # Import the Image and set its duration same as the audio (Insert the location 
    #of your photo instead of photo.jpg)
    clip = ImageClip(eclipse_image_file).set_duration(audio.duration)
    # Set the audio of the clip
    clip = clip.set_audio(audio)
    # Export the clip
    clip.write_videofile(video_filename, 
                         codec='libx264', 
                         audio_codec='aac', fps=24)

    if verbose:
        if os.path.isfile(video_filename): print("Success! : "+video_filename)
        else:print("Failure! : "+video_filename)

def escsp_make_clips(folders, youtube_folder,verbose=False):
    
#templade for an FFMPEG call to make a mp4 movie from a still image and a sound file.
    
    for folder in folders:
        #ESID=filename_2_ESID(os.path.basename(folder))
        if verbose: print("folder= "+folder)
        ESID=filename_2_ESID(folder)
        if verbose: print("ESID#= "+ESID)
        #eclipse_data_csv=os.path.join(folder, "eclipse_data.csv")
        eclipse_data_csv=glob.glob(os.path.join(folder,"*eclipse_data.csv"))

        if verbose: 
                 print("##################################")
                 print(eclipse_data_csv)
                 print("Type")
                 print(type(eclipse_data_csv))
                 print(len(eclipse_data_csv))
                 print("##################################")

        #If multiple eclipse_data_csv files, choose the first one 
        if type(eclipse_data_csv) == type([1,3]) and len(eclipse_data_csv) > 0:
            if verbose: 
                 print("##################################")
                 print(eclipse_data_csv)
                 print("Type")
                 print(type(eclipse_data_csv))
                 print(len(eclipse_data_csv))
                 print("##################################")
                 print(eclipse_data_csv)
            if eclipse_data_csv[0] == '' : 
                eclipse_data_csv=''
                if verbose: 
                    print("##################################")
                    print(eclipse_data_csv)
                    print("Type")
                    print(type(eclipse_data_csv))
                    print(len(eclipse_data_csv))
                    print("##################################")
            else: 
                 eclipse_data_csv=eclipse_data_csv[0] 
                 if verbose: 
                    print("##################################")
                    print(eclipse_data_csv)
                    print("Type")
                    print(type(eclipse_data_csv))
                    print(len(eclipse_data_csv))
                    print("##################################")
             
        if type(eclipse_data_csv) == type([1,3]) and len(eclipse_data_csv) == 0:
              eclipse_data_csv=''
             
        spreadsheet_exist=os.path.isfile(eclipse_data_csv)

        if spreadsheet_exist : 

            #time_format="%Y-%m-%d %H:%M:%S"
            eclipse_info=escsp_read_eclipse_csv(eclipse_data_csv, verbose=verbose)


            eclipse_type=eclipse_info["Eclipse_type"]
            eclipse_time_trio=escsp_get_eclipse_time_trio(eclipse_info, verbose=verbose)

#Get all of the recording files at the site
            recording_files=glob.glob(os.path.join(folder,"*."+"WAV"))
            eclipse_files=None
            two_days_before_files=None
            one_day_before_files=None


            if verbose: print("Number of audio files+ "+str(len(recording_files)))                         

            two_days_before_files=get_files_between_times(recording_files, eclipse_time_trio["two_days_before_start_time"],  
                                                          eclipse_time_trio["two_days_before_end_time"])
            one_day_before_files=get_files_between_times(recording_files, eclipse_time_trio["one_day_before_start_time"], 
                                                         eclipse_time_trio["one_day_before_end_time"])
            eclipse_files=get_files_between_times(recording_files, eclipse_time_trio["eclipse_start_time"], 
                                                  eclipse_time_trio["eclipse_end_time"])

            eclipse_date_str=eclipse_info["FirstContactDate"]
            if eclipse_files: 
                if verbose: print("youtube_folder= "+youtube_folder)
                clip_basename="ESID#"+str(ESID)+"_"+eclipse_type+"_"+eclipse_date_str+"_eclipse_3minute"
                clip_title=clip_basename.replace('_', ' ')
                if verbose: print("clip_basename= "+clip_basename)
                if verbose: print("clip_title= "+clip_title)

                audio_filename=os.path.join(youtube_folder,clip_basename+".wav") 
                you_tube_filename=os.path.join(youtube_folder,clip_basename+".mp4")
                
                
                eclipse_image_file, Photo_Credit, Photo_Description=get_eclipse_images(ESID, 
                                                                                       eclipse_type=eclipse_type, 
                                                                                       user_images=user_images, 
                                                                                       verbose=verbose)

                #Make 3 minute audioclip
                eclipse_wav, fs_ecl=combine_wave_files(eclipse_files, verbose=verbose)
                wavfile.write(audio_filename, fs_ecl, eclipse_wav)
                escsp_mk_video_clip(audio_filename=audio_filename, eclipse_image_file=eclipse_image_file,
                        video_filename=you_tube_filename,verbose=verbose)
                Recording_Date=eclipse_time_trio["eclipse_start_time"].strftime('%Y-%m-%d')
                Recording_Start_Time=eclipse_time_trio["eclipse_start_time"].strftime('%H:%M')+ " UTC"
                Recording_type=eclipse_info["Eclipse_type"] + "Eclipse, day of the eclipse."
                description=escsp_mk_youtube_description(eclipse_info, Recording_Date,Recording_Start_Time,
                                 Recording_type, Photo_Credit,Photo_Description)
                
                escsp_mk_youtube_csv(you_tube_filename, clip_title, description, clip_basename, eclipse_info, youtube_folder)



            if two_days_before_files :
                eclipse_type="Non-Eclipse-Day"
                if verbose: print("youtube_folder= "+youtube_folder)
                clip_basename="ESID#"+str(ESID)+"_"+eclipse_type+"_"+eclipse_date_str+"_two_days_before_3minute"
                clip_title=clip_basename.replace('_', ' ')
                if verbose: print("clip_basename= "+clip_basename)
                if verbose: print("clip_title= "+clip_title)
                
                audio_filename=os.path.join(youtube_folder,clip_basename+".wav") 
                you_tube_filename=os.path.join(youtube_folder,clip_basename+".mp4")
                
                #Make 3 minute audioclip
                two_days_before_wav, fs_tdb = combine_wave_files(two_days_before_files, verbose=verbose)
                wavfile.write(audio_filename, fs_tdb, two_days_before_wav)

                
                eclipse_image_file, Photo_Credit, Photo_Description=get_eclipse_images(ESID, 
                                                                                       eclipse_type=eclipse_type, 
                                                                                       user_images=user_images, 
                                                                                       verbose=verbose)

                
                escsp_mk_video_clip(audio_filename=audio_filename, eclipse_image_file=eclipse_image_file,
                        video_filename=you_tube_filename,verbose=verbose)
                Recording_Date=eclipse_time_trio["two_days_before_start_time"].strftime('%Y-%m-%d')
                Recording_Start_Time=eclipse_time_trio["two_days_before_start_time"].strftime('%H:%M')+ " UTC"
                Recording_type=eclipse_info["Eclipse_type"] + "Eclipse, two days before the eclipse."
                
                description=escsp_mk_youtube_description(eclipse_info, Recording_Date,Recording_Start_Time,
                                 Recording_type, Photo_Credit,Photo_Description)
                escsp_mk_youtube_csv(you_tube_filename, clip_title, description, clip_basename, eclipse_info, youtube_folder)


            if one_day_before_files: 
                eclipse_type="Non-Eclipse-Day"
                clip_basename="ESID#"+str(ESID)+"_"+eclipse_type+"_"+eclipse_date_str+"_one_day_before_3minute"
                clip_title=clip_basename.replace('_', ' ')
                if verbose: print("clip_basename= "+clip_basename)
                if verbose: print("clip_title= "+clip_title)
                
                audio_filename=os.path.join(youtube_folder,clip_basename+".wav") 
                you_tube_filename=os.path.join(youtube_folder,clip_basename+".mp4")

                #Make 3 minute audioclip
                one_day_before_wav, fs_odb = combine_wave_files(one_day_before_files)                
                wavfile.write(audio_filename, fs_odb, one_day_before_wav)

                eclipse_image_file, Photo_Credit, Photo_Description=get_eclipse_images(ESID, 
                                                                                       eclipse_type=eclipse_type, 
                                                                                       user_images=user_images, 
                                                                                       verbose=verbose)

                
                escsp_mk_video_clip(audio_filename=audio_filename, eclipse_image_file=eclipse_image_file,
                        video_filename=you_tube_filename,verbose=verbose)
                Recording_Date=eclipse_time_trio["one_day_before_start_time"].strftime('%Y-%m-%d')
                Recording_Start_Time=eclipse_time_trio["one_day_before_start_time"].strftime('%H:%M')+ " UTC"
                Recording_type=eclipse_info["Eclipse_type"] + "Eclipse, one day before the eclipse."
                
                description=escsp_mk_youtube_description(eclipse_info, Recording_Date,Recording_Start_Time,
                                 Recording_type, Photo_Credit,Photo_Description)
                escsp_mk_youtube_csv(you_tube_filename, clip_title, description, clip_basename, eclipse_info, youtube_folder)
                
           
        else:
            print("Error. Folder: "+folder+" No Spreadsheet.")

def escsp_replace_am_header(df):
    """
    Replace the header (column names) in a pandas DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame whose header is to be replaced.
    new_header (list): A list containing the new column names.
    
    Returns:
    pd.DataFrame: The DataFrame with the updated column names.
    """
    new_header = [(                 'AudioMoth ES ID Number', ...),
            (                   'AudioMoth \nSerial #', ...),
            (                         'Recepient Type', ...),
            (                          'Annular\n2023', ...),
            (                            'Total\n2024', ...),
            (                         'Recipient Name', ...),
            (                      'Recipient Address', ...),
            (                                  'Email', ...),
            (                                   'Sent', ...),
            (                          'Data Received', ...),
            (                    'Total to this group', ...),
            (       'Data Expected \nAnnular Eclipse ', ...),
            (                          'Internal Data', ...),
            (                    'Unnamed: 13_level_0', ...),
            (                    'Unnamed: 14_level_0', ...),
            (                    'Unnamed: 15_level_0', ...),
            (                    'Unnamed: 16_level_0', ...),
            (                  'Complete / Incomplete', ...),
            ('Required Data Collector Steps Complete?', ...),
            (                                 'Mailer', ...),
            (                    'Unnamed: 20_level_0', ...),
            (                    'Unnamed: 21_level_0', ...),
            (                    'Unnamed: 22_level_0', ...),
            (                    'Unnamed: 23_level_0', ...),
            (                          'Online Survey', ...),
            (                    'Unnamed: 25_level_0', ...),
            (   'What does this mean for the project?', ...),
            (                               'Latitude', ...),
            (                              'Longitude', ...),
            (         'Start time\n(Recorded by user)', ...),
            (                    'Unnamed: 30_level_0', ...),
            (                    'Unnamed: 31_level_0', ...),
            (                    'Unnamed: 32_level_0', ...),
            (                    'Unnamed: 33_level_0', ...)], 

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input df must be a pandas DataFrame")
    
    if not isinstance(new_header, list):
        raise ValueError("Input new_header must be a list")
    
    if len(new_header) != len(df.columns):
        raise ValueError("Length of new_header must match the number of columns in the DataFrame")
    
    df.columns = new_header
    return df

def escsp_sn2esid(file_path, AM_df):
    """
    Find the ESID number of the AudioMoth with the Serial Number contained with in a CONFIG.TXT file.
    
    Parameters:
    file_path (string): Full path to the CONFIG.TXT file.
    AM_df (pd.DataFrame): A data frame with the serialn # and ESID information.
    
    Returns:
    ESID (string): A string of the ESID number associated with the Serial Number contained in the CONFIG.TXT file
    """
    if os.path.exists(file_path):
       config_info_list=read_am_config(file_path)
       row=AM_df.loc[AM_df['AudioMoth Serial #'] == config_info_list["Device ID"] ]
       if len(row) > 0. :
           return str(row["AudioMoth ES ID Number"].values[0])
       else:
           print("Serial Number "+config_info_list["Device ID"]+" is not in the AudioMoth database.")
           return False

    else:
           print("No CONFIG.TXT file found")
           return False

def split_wave_files(indir, outdir, duration=60, verbose=False):
    """
    Split a large WAV file into segments and update the metadata.
    
    Parameters:
    indir (str): Path to the folder containing input WAV file.
    outdir (str): Directory to save the output segments.
    duration (int): Length of each segment in seconds (default is 60 seconds).
    verbose (bool): If True, execute print statements for debugging 
    """
    error_log=[]
    input_files=glob.glob(os.path.join(indir,"*."+"WAV"))
    input_files=natsorted(input_files)
    if verbose: print("Number of files to split= "+str(len(input_files)))   
    for input_file in input_files:
        if verbose: print("Working on file: "+input_file)
        file_size = os.path.getsize(input_file)
        
        if file_size > 1024:
            try :
                # Read the input WAV file
                sample_rate, data = wavfile.read(input_file)
    
                # Calculate the number of samples per segment
                samples_per_segment = duration * sample_rate
                if verbose: print("samples_per_segment: "+str(samples_per_segment))
    
                # Create the output directory if it doesn't exist
                if not os.path.exists(outdir):
                    os.makedirs(outdir)
    
                # Open the original WAV file to read metadata
                with wave.open(input_file, 'rb') as wave_file:
                    params = wave_file.getparams()
    
                # Split the data into segments
                total_samples = len(data)
                num_segments = total_samples // samples_per_segment
                if verbose: print("input_file: "+input_file)
                next_time=filename_2_datetime(os.path.basename(input_file), 
                                              verbose=verbose)[0]
                
                if verbose: print(type(next_time))
                if type(next_time) == "list":
                    if verbose: print(type(next_time))
                    next_time=next_time[0]
                    if verbose: print(type(next_time))
    
                for i in range(num_segments + 1):

                    start_sample = i * samples_per_segment
                    end_sample = start_sample + samples_per_segment
        
                    if end_sample > total_samples:
                                                                                                                            end_sample = total_samples
        
                    segment_data = data[start_sample:end_sample]
        
                    # Write the segment to a new WAV file
            
                    time_format="%Y%m%d_%H%M%S"
                    next_time_str = next_time.strftime(time_format) 
                    segment_file = os.path.join(outdir, next_time_str+".WAV")
                    if verbose: print("Outfile= "+ segment_file)
                    with wave.open(segment_file, 'wb') as wave_segment:
                        wave_segment.setparams(params)
                        wave_segment.writeframes(segment_data.tobytes())

                    next_time=next_time+datetime.timedelta(seconds=duration)
                    if verbose: print("Working on file: "+input_file)
                    if verbose: print(f"Segment {i+1} written to {segment_file}")
            except: #except
                error="Could not split file: "+input_file+" into "+str(duration)+" second segments."
                if verbose: print(error)
                error_log.append(error)
        else:
            error="File size of "+input_file+" was "+str(file_size)+" bytes which is less than the one kb filter."
            if verbose: print(error)
            error_log.append(error)

    if len(error_log) > 0:
        file_path=os.path.join(outdir, "ERROR_LOG_split_wave_files.txt")
        if verbose: print("Error Log = "+file_path)
             
        with open(file_path, 'a') as file:
            print("Time of ERROR LOG= "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            file.write("Time of ERROR LOG= "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
            for error in error_log:
                file.write(error + '\n')
            file.write("End of Log" + '\n')
            file.write("##############################################" + '\n')
            file.close()
        
def datetime_2_filename(datetimeObj, AudioMoth=True):
    if AudioMoth == True:
        time_format="%Y%m%d_%H%M%S"
    
    filename_out=datetimeObj.strftime(time_format)+".WAV"
    return filename_out      

def Reports_1(folder, TOTAL=True, verbose=False, save=False):


    # Define the column headings
    if TOTAL:
        columns = [
             "ESID #", 
             "Config file Present = No, 1 = yes",
             "GB of data", 
             "AM Timestamp Set",
             "Eclipse Data File Present",
             "Three Days of Data Recorded? (Two days before and Eclipse Day 0 = No, 1 = yes)",
             "April 6, 2024 Data 0 = No, 1 = yes",
             "April 7, 2024 Data 0 = No, 1 = yes",
             "April 8, 2024 Data 0 = No, 1 = yes", 
             "April 9, 2024 Data 0 = No, 1 = yes",
             "April 10, 2024 Data 0 = No, 1 = yes", 
             "April 11, 2024 Data 0 = No, 1 = yes"
             ]
        
        dates=[
             "2024, 4, 6, 0", "2024, 4, 6, 23",
             "2024, 4, 7, 0", "2024, 4, 7, 23",
             "2024, 4, 8, 0", "2024, 4, 8, 23",
             "2024, 4, 9, 0", "2024, 4, 9, 23",
             "2024, 4, 10, 0", "2024, 4, 10, 23",
             "2024, 4, 11, 0", "2024, 4, 11, 23"
             ]
    else:          
        columns = [
             "ESID #", 
             "Config file Present = No, 1 = yes",
             "GB of data", 
             "AM Timestamp Set",
             "Eclipse Data File Present",
             "Three Days of Data Recorded? (Two days before and Eclipse Day 0 = No, 1 = yes)",
             "October 12, 2023 Data 0 = No, 1 = yes",
             "October 13, 2023 Data 0 = No, 1 = yes",
             "October 14, 2023 Data 0 = No, 1 = yes", 
             "October 15, 2023 Data 0 = No, 1 = yes",
             "October 16, 2023 Data 0 = No, 1 = yes", 
             "October 17, 2023 Data 0 = No, 1 = yes"
             ]
        
        dates=[
             "2023, 10, 12, 0", "2023, 10, 12, 23",
             "2023, 10, 13, 0", "2023, 10, 13, 23",
             "2023, 10, 14, 0", "2023, 10, 14, 23",
             "2023, 10, 15, 0", "2023, 10, 15, 23",
             "2023, 10, 16, 0", "2023, 10, 16, 23",
             "2023, 10, 17, 0", "2023, 10, 17, 23"
             ]

    #Get ESID #
    site_values={columns[0] : filename_2_ESID(folder)}

    #Is there a CONFIG.TXT file?
    file_list = os.listdir(folder)
    if "CONFIG.TXT" in file_list: 
         site_values[columns[1]]=1
    else:
         site_values[columns[1]]="N/A"

    #Get size of data in the folder in GB str(round(answer, 2))
    site_values[columns[2]]=str(round(get_folder_size_in_gb(folder),2))

    
    #if site_values[columns[1]] == 1: 
    if True :
         if AM_timestamp_set(folder) == True:
            site_values[columns[3]]=1
            
            
            eclipse_data_csv=os.path.join(folder, 'eclipse_data.csv')
            
             
            spreadsheet_exist=os.path.isfile(eclipse_data_csv)

            if spreadsheet_exist :
                site_values[columns[4]]=1
                #time_format="%Y-%m-%d %H:%M:%S"
                eclipse_info=escsp_read_eclipse_csv(eclipse_data_csv, verbose=verbose)

                recording_files=glob.glob(os.path.join(folder,"*.WAV"))
                eclipse_files=None
                two_days_before_files=None
                one_day_before_files=None


                if verbose: print("Number of audio files+ "+str(len(recording_files)))                         

                eclipse_time_trio=escsp_get_eclipse_time_trio(eclipse_info, verbose=verbose)
                two_days_before_files=get_files_between_times(recording_files, eclipse_time_trio["two_days_before_start_time"],  
                                                          eclipse_time_trio["two_days_before_end_time"])
                one_day_before_files=get_files_between_times(recording_files, eclipse_time_trio["one_day_before_start_time"], 
                                                         eclipse_time_trio["one_day_before_end_time"])
                eclipse_files=get_files_between_times(recording_files, eclipse_time_trio["eclipse_start_time"], 
                                                  eclipse_time_trio["eclipse_end_time"])
                
                
                #All Three Days of recording
                if two_days_before_files and one_day_before_files and eclipse_files:
                     site_values[columns[5]]=1
                else: site_values[columns[5]]=0
                
                #One Day Before "0 = No, 1 = yes",
                if two_days_before_files:
                     site_values[columns[6]]=1
                else: site_values[columns[6]]=0
                #One Day Before "0 = No, 1 = yes",
                if one_day_before_files:
                     site_values[columns[7]]=1
                else: site_values[columns[7]]=0 
                #Day of "0 = No, 1 = yes",
                if eclipse_files:
                     site_values[columns[8]]=1
                else: site_values[columns[8]]=0

            else:
               site_values[columns[4]]=0
               site_values[columns[5]]="N/A"
               site_values[columns[6]]="N/A"
               site_values[columns[7]]="N/A"
               site_values[columns[8]]="N/A"

            #One Day After "0 = No, 1 = yes",
            if times_between_dates(folder, dates[6], dates[7]):
                site_values[columns[9]]=1
            else:
                site_values[columns[9]]=0
            #Two Days After "0 = No, 1 = yes",
            if times_between_dates(folder, dates[8], dates[9]): 
                site_values[columns[10]]=1
            else:
                site_values[columns[10]]=0
            #Three Days After "0 = No, 1 = yes",
            if times_between_dates(folder, dates[10], dates[11]): 
                site_values[columns[11]]=1
            else:
                site_values[columns[11]]=0

            
         else:
              site_values[columns[3]]=0
              site_values[columns[4]] ="N/A"
              site_values[columns[5]] ="N/A"
              site_values[columns[6]] ="N/A"
              site_values[columns[7]] ="N/A"
              site_values[columns[8]] ="N/A"
              site_values[columns[9]] ="N/A"
    

         
    else:
        site_values[columns[3]] ="N/A"
        site_values[columns[4]] ="N/A"
        site_values[columns[5]] ="N/A"
        site_values[columns[6]] ="N/A"
        site_values[columns[7]] ="N/A"
        site_values[columns[8]] ="N/A"
        site_values[columns[9]] ="N/A"

    #return site_values
    df=pd.DataFrame.from_dict([site_values])

    # Define the output CSV file path
    output_file_path = os.path.join(folder,'Report_1.csv')

    #Save the DataFrame to a CSV file
    if save:
         df.to_csv(output_file_path, index=False)

    if verbose: print(f"DataFrame saved to {output_file_path}")   

    return df 
    
def AM_timestamp_set(folder, verbose=False):
    file_list = glob.glob(os.path.join(folder,"*."+"WAV"))
    """
    Split a large WAV file into segments and update the metadata.
    
    Parameters:
    folder (str): Path to the folder containing input WAV files.
    verbose (bool): If True, execute print statements for debugging 
    """

    am_time_set=False

    datetime_list=filename_2_datetime(file_list, verbose=verbose)
    if verbose: print(file_list)
    if verbose: print(folder)
    if verbose: print(datetime_list) 
    start_datetime=datetime.datetime(2023, 10, 1, 0, 0, 0)
    end_datetime=datetime.datetime(2024, 4, 11, 0, 0, 0)
    if datetime_list != None:
        am_time_set=any(start_datetime <= dt <= end_datetime for dt in datetime_list)
    else: am_time_set=False

    return am_time_set

def times_between_dates(folder, start, end, verbose=False):
    file_list = glob.glob(os.path.join(folder,"*."+"WAV"))
    am_time_set=False
    start_elements=start.split(",")
    if verbose: print(start_elements)
    end_elements=end.split(",")
    if verbose: print(end_elements)
    datetime_list=filename_2_datetime(file_list)
    start_datetime=datetime.datetime(int(start_elements[0]), int(start_elements[1]), int(start_elements[2]), int(start_elements[3]))
    end_datetime=datetime.datetime(int(end_elements[0]), int(end_elements[1]), int(end_elements[2]), int(end_elements[3]))
    am_time_set=any(start_datetime <= dt <= end_datetime for dt in datetime_list)

    return am_time_set

def get_folder_size_in_gb(folder_path):
    """
    Calculate the total size of a folder in gigabytes.
    
    Parameters:
    folder_path (str): The path to the folder.
    
    Returns:
    float: The size of the folder in gigabytes.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Skip if it's a broken symlink
            if not os.path.islink(file_path) and os.path.exists(file_path):
                total_size += os.path.getsize(file_path)
    
    # Convert bytes to gigabytes
    total_size_gb = total_size / (1024 ** 3)
    return total_size_gb

def get_youtube_link(stdout, verbose=False):
    if type(stdout) == type([]):
         text=stdout[0]
    if type(stdout) == type('a'):
         text=stdout

    # Regular expression to find the Video Id
    match_link = re.search(r"Video id\s+'([^']+)'", text)
    
    if verbose: print("match_link type = "+type(match_link))

    if match_link:
        video_id = match_link.group(1)
        video_id.replace("'", "")
        video_id.strip()
        return_value="https://youtu.be/"+video_id
        if verbose: print(f"Extracted Video ID: {video_id}")
    else:
        return_value=None
        if verbose: print("No Video ID found.")

    return return_value

def eclipse_data_all_to_esid_dirs(input_csv, output_top_dir, 
                                  folder_suffix="_AnnularEclipse_AudioMothTimeChime_Split",
                                  verbose=False):
    """
    Read an eclipse_data CSV file made from Joel's Eclipse Data Tool with "ESID" added to the first
      column into a pandas DataFrame and save each row to a separate eclipse_data.csv file in a directory
      based on ESID.
    
    Args:
    - input_csv (str): Path to the input CSV file.
    - output_top_dir (str): Top level directory where the rows of the initial eclipse_data_all file 
        will be saved as individual eclipse_data.csv files in ESID subfolders.
    - verbose: If set, print statements will be executed.
    Returns:
    - None
    """
   
    # Read the input CSV file into a DataFrame
    dataframe = pd.read_csv(input_csv)
    
    # Iterate over each row in the DataFrame
    for index, row in dataframe.iterrows():
        # Convert the row to a DataFrame
        row_df = row.to_frame().T

        #Get ESID string
        ESID=row_df["ESID"].values[0]
        if verbose: print(ESID, type(ESID))
        if type(ESID) == type([0]): ESID=ESID[0]
        if type(ESID) == type('a') and len(ESID) < 3:
            suffix=''
            if "A" in ESID: 
                 suffix="A"
                 ESID=ESID.strip("A")
            if "B" in ESID: 
                 suffix="B"
                 ESID=ESID.strip("B")
            if "a" in ESID: 
                 suffix="a"
                 ESID=ESID.strip("a")
            if "b" in ESID: 
                 suffix="b"
                 ESID=ESID.strip("b")

            if len(ESID) == 2:ESID="0"+ESID+suffix
            if len(ESID) == 1:ESID="0"+ESID+suffix

        if type(ESID) == type(int(1)):
             ESID=str(f"{ESID:03d}")
        if type(ESID) == type(float(1)):
             ESID=str(f"{ESID:03d}")

        if verbose: print(ESID, type(ESID))

        row_df["ESID"].values[0]=ESID
        
             
        output_dir=os.path.join(output_top_dir, "ESID#"+ESID+folder_suffix)
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
    
        # Define the output file path
        output_file = os.path.join(output_dir, "eclipse_data.csv")
        # If and eclipse_data.csv file exists, move it
        if os.path.exists(output_file):
             now = datetime.datetime.now() # current date and time
             time_stamp=now.strftime("%Y%m%d_%H%M%S")
             new_file=output_file.strip(".csv")+"_"+time_stamp+".oldcsv"

             shutil.move(output_file, new_file)
        
        # Save the row DataFrame to a CSV file
        row_df.to_csv(output_file, index=False)
        
        if verbose: print(f"Saved eclispe_data.csv to '{output_dir}'.")


