if __name__ == "__main__":
    print("Eclipse Soundscapes: Citizen Science Project Library")

"""escsp.py Library for the Eclipse Soundscapes: Citizen Science Project"""
###########################################################################
#Import Libraries section
import numpy as np 
# for visualizing the data 
#file handling and misc.
import os  
import datetime
import pandas as pd
from natsort import natsorted
import glob
import numpy as np 
# for visualizing the data 
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
import subprocess
from tracemalloc import stop
# for opening the media file 
import scipy.io.wavfile as wavfile
import wave
from scipy.misc import derivative
from scipy.interpolate import interp1d
import copy
#import moviepy
from moviepy import *
import re
import scipy
import pytz
###########################################################################
#Global Variables section
user_images=None
youtube_assets_folder="./YouTube_Assets/"
privacyStatus="private"
#privacyStatus="public"

AM_Spreadsheet=os.getenv("total_redacted_AM_spreadsheet")
###########################################################################
#Function Definitions Section
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
    """ 
    Return recording start time information for a wave file based on the filename. 
    Start time and date returned using datetime format.
    NPS Files return: start_time, start_date, site_name 
    
    
    """
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

def escsp_read_eclipse_csv(eclipse_data_csv, verbose=False, ESID=False):
    """
    Extracts the row from a CSV file where the 'AudioMoth ES ID Number' matches a given string,
    and returns the columns as a dict 

    Args:
    - csv_file (str): Path to the CSV file.
    - esid_string (str): The ESID string to match.
    
    Returns:
    - eclipse_info (dict): A ditionary containing the matching row(s), or None alse if no match is found."""
    eclipse_info=None
    df=None

    if os.path.isfile(eclipse_data_csv) :
        if verbose: print("escsp_read_eclipse_csv success! " + eclipse_data_csv) 
        if verbose:
            print("Type ESID= "+str(type(ESID)))
            print("ESID= "+str(ESID))
        if ESID:
            if type(ESID) == type('a'):
                if verbose: print("ESID is of string type= "+ESID) 
            else:
                print("esid was not a string attempting to fix.")
                print("esid was= "+str(ESID)+", "+type(ESID).__name__)
                ESID=str(ESID).zfill(3)
                print("esid_string now= "+ESID)

    # Read the CSV file into a DataFrame
            df = extract_row_by_esid(eclipse_data_csv, esid_string=ESID, verbose=verbose)
            if verbose: 
                print("Type df= "+str(type(df)))
        else:
            df=pd.read_csv(eclipse_data_csv, header=[0])
        #Doing in this way instead of using df.to_dict to make a simpler dictionary
        verbose=1
        if verbose: 
            if  type(df).__name__ =='DataFrame'  :
                print("Data frame column names (keys):")
                print(df.columns)
            else:  print("df for ESID "+str(ESID)+" is None")
        if  type(df).__name__ =='DataFrame'  :
            eclipse_info={
                "ESID": str(df['AudioMoth ES ID Number'].values[0]).zfill(3), 
                "Latitude":df["Latitude"].values[0], 
                "Longitude" :df["Longitude"].values[0],
                "Eclipse_type" :df["LocalType"].values[0], 
                "CoveragePercent" :df["CoveragePercent"].values[0], 
                "FirstContactDate" :df["FirstContactDate"].values[0], 
                "FirstContactTimeUTC" :df["FirstContactTimeUTC"].values[0], 
                "SecondContactTimeUTC" :df["SecondContactTimeUTC"].values[0], 
                "ThirdContactTimeUTC" :df["ThirdContactTimeUTC"].values[0], 
                "FourthContactTimeUTC" :df["FourthContactTimeUTC"].values[0], 
                "MaxEclipseTimeUTC" :df["TotalEclipseTimeUTC"].values[0]
                }
        else:
            print("ESID not found.")

    else:
        print('Error! No file named '+eclipse_data_csv)

    return eclipse_info

def escsp_get_eclipse_time_trio(eclipse_info, verbose=False):
    time_format="%Y-%m-%d %H:%M:%S"
    eclipse_type=eclipse_info["Eclipse_type"]
    if eclipse_type == "Annular" or eclipse_type == "Total":
        second_contact=eclipse_info["FirstContactDate"] + " " +eclipse_info["SecondContactTimeUTC"] 
        if verbose: print("eclipse_type: " + eclipse_type)
         
        if verbose: print(second_contact)
        eclipse_start_time = datetime.datetime.strptime(second_contact, time_format) 
#set the eclipse end time
        third_contact = eclipse_info["FirstContactDate"] + " " +eclipse_info["ThirdContactTimeUTC"] 
        eclipse_end_time =  datetime.datetime.strptime(third_contact, time_format) 

    else: #Set the range to be 3 minutes before and after the eclipse.
        max_eclipse= datetime.datetime.strptime(eclipse_info["FirstContactDate"] + 
                                                " " +eclipse_info["MaxEclipseTimeUTC"], 
                                                time_format)
        eclipse_start_time=max_eclipse-datetime.timedelta(minutes=1.5)
        eclipse_end_time=max_eclipse+datetime.timedelta(minutes=1.5)

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
    """ 
    Return a list if datetimes that correspond to the name of a WAV file
    """
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
    """Return only the filepaths for the recording files that are between the start_time-1 minute & the end_time+1 minute"""

    #I know there is a better way (more matrix) to do this, but I don't have the time to figure it out.
    return_files=[]
    one_minute=datetime.timedelta(minutes=1)
    for file in files:
        date_and_time=filename_2_datetime(file, file_type="AudioMoth")
        date_and_time=date_and_time[0]
        if date_and_time >= start_time-one_minute and date_and_time <= end_time+one_minute: 
            return_files.append(file)

    #return_files=natsorted(return_files)
    return return_files

def combine_wave_files(files, start_time=False, end_time=False, verbose=None):
    """Open the wave files in the list 'files' and combine them into one long wave file"""
    
    audio=False
    Fs_original=False

    Files_start_dt=filename_2_datetime(files[0])[0]
    Files_end_dt=filename_2_datetime(files[len(files)-1])[0]+datetime.timedelta(minutes=1)

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
    if start_time:
        diff_between_starts=start_time-Files_start_dt
        trim_start=int(diff_between_starts.total_seconds()*Fs_original)
    else:
        trim_start=int(0)
    
    if end_time:
        diff_between_ends=Files_end_dt-end_time
        trim_end=int(len(audio)-int(1)-int(diff_between_ends.total_seconds()*Fs_original))
    else:
         trim_end=int(len(audio)-1)
    

    audio=audio[trim_start:trim_end]

    return audio, Fs_original

def adjust_am_datetime(files, start_time,  time_zone_value, 
                       time_str="%Y-%m-%d %H:%M:%S", 
                       updated_folder=False, 
                       verbose=False):
    """Program to adjust the time of AudioMoth files if the time was not properly set. 
    Requires a set of recording files and a datetime object of the reported start time.

    Args:
    - files list of files to adjust to the the first start-time
    - start_time= String of the time that the first "real" recording was taken.
    - updated_folder (str): Folder to copy the WAV file to with the updated timestamp
    - verbose
    - 

    Returns:
    - 
    - 
      
    """

    if verbose:
        print("start_time: "+start_time)
        print("time_zone_value: "+time_zone_value)
        print("time_str" + time_str)

    
    recorded_time_dt=datetime.datetime.strptime(start_time, time_str)
    time_zone = pytz.timezone(time_zone_value)
    recorded_time_dt=time_zone.localize(recorded_time_dt)
    utc_time = recorded_time_dt.astimezone(pytz.UTC)

    files=natsorted(files)
    first_real_file_found=0
    updated_file_names=[]

    if len(files) >= 1:
        
        for file in files:  
            if verbose: print("File= "+ file)
            if os.path.getsize(file) < 5760080:
                updated_file_names.append('')
            
            else:
                d_and_t_0=filename_2_datetime(file, file_type="AudioMoth")[0]
                d_and_t_0=time_zone.localize(d_and_t_0)
                if first_real_file_found == 0:
                    time_shift=utc_time-d_and_t_0
                    first_real_file_found=1

                updated_file_name = datetime_2_filename(time_shift + d_and_t_0, AudioMoth=True)
                updated_file_names.append(updated_file_name)

                if verbose:
                    print("original_file_name: " + file)
                    print("updated_file_name: " + updated_file_name)
                    print("updated_path: " + os.path.join(updated_folder, updated_file_name))


                if updated_folder:
                    if not os.path.isdir(updated_folder):
                        os.makedirs(updated_folder)
                    command_line="cp "+file+" "+os.path.join(updated_folder, updated_file_name)
                    os.system(command_line)
                    if verbose:
                        print("Original_file_name: " + file)
                        print("Saved file: "+os.path.join(updated_folder, updated_file_name))

    else:
        if verbose:
            print("No files submitted")
        updated_file_names=None  

    return updated_file_names #updated_file_names

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
             
   
    return str(esid).zfill(3)

def escsp_get_psd(folder, plots_folder, filelist=None, 
                  eclipse_type = "Total", verbose=False, 
                  eclipse_data_csv=False, Hertz=False,
                  relative_psd_csv=False,
                  new_relative_psd_csv=False,
                  spreadsheets_folder=False,
                  wave_folder=False,
                  old_plots=False):
    
    if verbose: print("eclipse_data_csv = "+eclipse_data_csv)
    if verbose: print(folder)
    ESID=filename_2_ESID(folder)
    if verbose: print("ESID #=" + ESID)
    plot_1_name=os.path.join(plots_folder, "PSD_plot_Welch_ESID#"+ESID+".png")
    if verbose: print("plot_1_name= "+plot_1_name)
    plot_1a_name=os.path.join(folder, "PSD_plot_Welch_ESID#"+ESID+".png")

    #Welch and Ba rtlet plots
    plot_2a_name=os.path.join(plots_folder, "PSD_W_and_B_plot_ESID#"+ESID+".png")
    if verbose: print("plot_2a_name (Welch)= "+plot_2a_name)
    plot_2b_name=os.path.join(plots_folder, "PSD_Bartlett_plot_ESID#"+ESID+".png")
    if verbose: print("plot_2b_name (Bartlett)= "+plot_2b_name)
    #Eclipse Day over average plots
    plot_3a_name=os.path.join(plots_folder, "PSD_Average_plot_ESID#"+ESID+".png")
    if verbose: print("plot_3a_name (Average)= "+plot_3a_name)
    plot_3b_name=os.path.join(folder, "PSD_Average_plot_ESID#"+ESID+".png")
    if verbose: print("plot_3b_name (Average)= "+plot_3b_name)
    #Eclipse Day over average plots in the cricket frequencies
    plot_4a_name=os.path.join(plots_folder, "PSD_Average_plot_ESID#"+ESID+"_2-8_kHz.png")
    if verbose: print("plot_4a_name (Average)= "+plot_4a_name)
    plot_4b_name=os.path.join(folder, "PSD_Average_plot_ESID#"+ESID+"_2-8_kHz.png")
    if verbose: print("plot_4b_name (Average)= "+plot_4b_name)
    plot_5a_name=os.path.join(plots_folder, "Relative_PSD_plot_ESID#"+ESID+"_2-8_kHz.png")
    if verbose: print("plot_5a_name (Average)= "+plot_5a_name)
    plot_6a_name=os.path.join(plots_folder, "Relative_Power_plot_ESID#"+ESID+"_2-8_kHz.png")
    if verbose: print("plot_6a_name (Average)= "+plot_6a_name)
    csv_6a_name=os.path.join(plots_folder, "Relative_Power_and_Times_ESID#"+ESID+"_2-8_kHz.csv")



    #set the range for crickets [2 to 8 kHz]
    cricket_freq_range=[2000., 8000.]

    if Hertz:
        to_kHz=1
        x_axis_freq_label='frequency [Hertz]'
        y_axis_freq_label='Power Spectral Density[Pascals^2$/Hz]'
    else:
        to_kHz=1000.
        x_axis_freq_label='frequency [kiloHertz]'
        y_axis_freq_label='Power Spectral Density[Pascals^2$/kHz]'
    ###########################################################################
    out_text=str(ESID).zfill(3)+",,,,,,,,,,,,\n"
    ###########################################################################
    #Need to change this to an if statement after testing
    #eclipse_data_csv=os.path.join(folder, "eclipse_data.csv")

    if os.path.isfile(eclipse_data_csv) :
        eclipse_info=escsp_read_eclipse_csv(eclipse_data_csv, ESID=ESID, verbose=verbose)
        eclipse_time_trio=escsp_get_eclipse_time_trio(eclipse_info, verbose=verbose)
        eclipse_local_type=eclipse_info["Eclipse_type"]
        if verbose: print(eclipse_info)
        df=pd.DataFrame(eclipse_info, index=[0])
        if verbose: print("success! " + eclipse_data_csv) 
        
        #eclipse_start_time=max_eclipse-datetime.timedelta(minutes=3)
        #eclipse_end_time=max_eclipse+datetime.timedelta(minutes=3)
        #second_contact=datetime.datetime.strftime(eclipse_start_time, time_format)
        #third_contact = datetime.datetime.strftime(eclipse_end_time, time_format)
        #df=pd.read_csv(eclipse_data_csv, header=[0])
        #time_format="%Y-%m-%d %H:%M:%S"
        #test=True
        #if type(df["SecondContactTimeUTC"].values[0]) != type("test"):
        #    test=False
        #eclipse_local_type= df['Eclipse_type'].values[0]
        #print("Eclipse Type= "+eclipse_local_type)
        #if eclipse_local_type == "NaN":
        #    test=False
        #if eclipse_local_type != "Annular" or eclipse_local_type != "Total": 
        #    test=False

        #if test :
        #if eclipse_type == "Annular" or eclipse_type == "Total":
        ###########################################################################
            #set the eclipse start time
        #    chars_to_remove=["\"", "\'", "[", "]"]


        #    second_contact=df["FirstContactDate"].values[0]+" "+df["SecondContactTimeUTC"].values[0]
        #    third_contact = df["FirstContactDate"].values[0]+" "+df["ThirdContactTimeUTC"].values[0]
        #    for char_to_remove in chars_to_remove:
        #        second_contact.replace(char_to_remove, '')
        #    print("Second Contact"+second_contact)

        #    eclipse_start_time = datetime.datetime.strptime(second_contact, time_format)
            ###########################################################################
            #
        #    for char_to_remove in chars_to_remove:
        #        third_contact.replace(char_to_remove, '')
        #    eclipse_end_time =  datetime.datetime.strptime(third_contact, time_format) 
        #else:
        #    max_eclipse=datetime.datetime.strptime(
        #        df["FirstContactDate"].values[0]+ " " + df["MaxEclipseTimeUTC"].values[0], time_format)
        #eclipse_start_time=max_eclipse-datetime.timedelta(minutes=3)
        #eclipse_end_time=max_eclipse+datetime.timedelta(minutes=3)
        #second_contact=datetime.datetime.strftime(eclipse_start_time, time_format)
        #third_contact = datetime.datetime.strftime(eclipse_end_time, time_format)

        #eclipse_year=str(eclipse_time_trio["eclipse_start_time"].year)
        eclipse_start_str=eclipse_time_trio["eclipse_start_time"].strftime("%Y-%B-%d_%H%M%S")+"_UTC".replace(" ", "")
        one_day_before_str=eclipse_time_trio["one_day_before_start_time"].strftime("%Y-%B-%d_%H%M%S")+"_UTC".replace(" ", "")
        two_days_before_str=eclipse_time_trio["two_days_before_start_time"].strftime("%Y-%B-%d_%H%M%S")+"_UTC".replace(" ", "")
        ########################################################################### 
        #DateTime elements
        #two_days_before_start_time=eclipse_start_time-datetime.timedelta(hours=48)
        #two_days_before_end_time=eclipse_end_time-datetime.timedelta(hours=48)

        #one_day_before_start_time=eclipse_start_time-datetime.timedelta(hours=24)   
        #one_day_before_end_time=eclipse_end_time-datetime.timedelta(hours=24)

        #two_days_before_start_time=eclipse_time_trio["two_days_before_start_time"]
        #two_days_before_end_time=eclipse_time_trio["two_days_before_end_time"]

        #one_day_before_start_time=eclipse_time_trio["one_day_before_start_time"]
        #one_day_before_end_time=eclipse_time_trio["one_day_before_end_time"]

        eclipse_start_time=eclipse_time_trio["eclipse_start_time"]
        eclipse_end_time=eclipse_time_trio["eclipse_end_time"]
        ########################################################################### 
        #DateTime strings
        second_contact=eclipse_time_trio["eclipse_start_time"].strftime("%Y-%B-%d %H%M%S")+"UTC".replace(" ", "")
        third_contact =eclipse_time_trio["eclipse_end_time"].strftime("%Y-%B-%d %H%M%S")+"UTC".replace(" ", "")
        ###########################################################################
        #Get all of the recording files at the site
        recording_files=glob.glob(os.path.join(folder,"*."+"WAV"))
        if verbose: print(len(recording_files))   

        
        eclipse_files=None
        two_days_before_files=None
        one_day_before_files=None                      

        freqs_out_ecl_wel=None
        freqs_out_odb_wel=None
        freqs_out_tdb_wel=None                     

        freqs_out_ecl_bart=None
        freqs_out_odb_bart=None
        freqs_out_tdb_bart=None
        ###########################################################################
        #This comes in handy when testing to see if an object is of array type
        test_arr=np.ndarray(shape=(2,2), dtype=float, order='F')
        ###########################################################################
        #Gather all if the .WAV files within the time frame of the eclipse
        #two_days_before_files=get_files_between_times(recording_files, two_days_before_start_time, two_days_before_end_time)     
        #one_day_before_files=get_files_between_times(recording_files, one_day_before_start_time, one_day_before_end_time)
        #eclipse_files=get_files_between_times(recording_files, eclipse_start_time, eclipse_end_time)

        two_days_before_files=get_files_between_times(recording_files, eclipse_time_trio["two_days_before_start_time"],  
                                                      eclipse_time_trio["two_days_before_end_time"])
        one_day_before_files=get_files_between_times(recording_files, eclipse_time_trio["one_day_before_start_time"], 
                                                     eclipse_time_trio["one_day_before_end_time"])
        eclipse_files=get_files_between_times(recording_files, eclipse_time_trio["eclipse_start_time"], 
                                              eclipse_time_trio["eclipse_end_time"])
        
        
        
        
        ###########################################################################
        #IF the filelist parameter is set, then write the names of the files to the filelst file.  
        if filelist:
            if os.path.isfile(filelist):
                list_file=filelist
            else:
                list_file=os.path.join(folder, "ESID#"+ESID+'_Analysis_Files.csv')
            
            if eclipse_files:
                df=pd.DataFrame({'Eclipse Files': eclipse_files}) 
                if two_days_before_files:
                    df.insert(1, 'Two Days Before Files', two_days_before_files, True)
                else: df=pd.DataFrame({'Two Days Before Files': ["None"]}) 
                if one_day_before_files:
                    df.insert(1, 'One Day Before Files', one_day_before_files, True)
                else: df=pd.DataFrame({'One Day Before Files': ["None"]})       

            else: 
                df=pd.DataFrame({'Eclipse Files': ["None"]})    
            
            df.to_csv(list_file, index=False)
        ###########################################################################
        #If there are are any .WAV files within the eclipse time on the eclipse day
        # then continue
        if eclipse_files: 
            eclipse_wav, fs_ecl=combine_wave_files(eclipse_files, 
                                                   start_time= eclipse_time_trio["eclipse_start_time"], 
                                                   end_time=eclipse_time_trio["eclipse_end_time"], 
                                                   verbose=None)
            #f0, eclipse_psd=scipy.signal.periodogram(eclipse_wav, fs_ecl)
            fig, ax =plt.subplots()
            ax.psd(eclipse_wav, Fs=fs_ecl, color="orange", label="Eclipse Day")
            plt.title("PSD Welch's Method "+ESID+" Eclipse on "+str(df["FirstContactDate"].values[0]))
            freqs_out_ecl_wel, eclipse_wav_psd_welch=calc_psd(eclipse_wav, fs_ecl)
            freqs_out_ecl_bart, eclipse_wav_psd_bart=calc_psd(eclipse_wav, fs_ecl, Bartlett=True)

            #Write write out file of data to be analyzed 
            ecl_data_start_time=filename_2_datetime(eclipse_files[0])[0].strftime("%Y-%B-%d_%H%M%S")+"_UTC".replace(" ", "")
            ecl_data_start_time=eclipse_start_str
            wav_file_name=os.path.join(wave_folder, 
                                          "ESID#"+ESID+"_"+ecl_data_start_time+".WAV")
            wavfile.write(wav_file_name, fs_ecl, eclipse_wav)
            ###########################################################################
            #If there are are any .WAV files within the eclipse time two days before the eclipse
            # then do this part
            if two_days_before_files :
                print("Length of filelist: " + str(len(two_days_before_files)))
                two_days_before_wav, fs_tdb = combine_wave_files(two_days_before_files, 
                                                   start_time= eclipse_time_trio["two_days_before_start_time"], 
                                                   end_time=eclipse_time_trio["two_days_before_end_time"], 
                                                   verbose=None)
                #f2, two_days_before_psd=scipy.signal.periodogram(two_days_before_wav, fs_tdb)
                ax.psd(two_days_before_wav, Fs=fs_tdb, color="green", label="Two Days Before")
                freqs_out_tdb_wel, tdb_wav_psd_welch=calc_psd(two_days_before_wav, fs_tdb)
                freqs_out_tdb_bart, tdb_wav_psd_bart=calc_psd(two_days_before_wav, fs_tdb, Bartlett=True)

                #Write write out file of data to be analyzed 
                tdb_data_start_time=filename_2_datetime(two_days_before_files[0])[0].strftime("%Y-%B-%d_%H%M%S")+"_UTC".replace(" ", "")

                tdb_data_start_time=two_days_before_str
                wav_file_name=os.path.join(wave_folder, 
                                           "ESID#"+ESID+"_"+tdb_data_start_time+".WAV")
                wavfile.write(wav_file_name, fs_tdb, two_days_before_wav)
            ###########################################################################
            #If there are are any .WAV files within the eclipse time one day before the eclipse
            # then continue
            if one_day_before_files: 
                one_day_before_wav, fs_odb = combine_wave_files(one_day_before_files, 
                                                   start_time= eclipse_time_trio["one_day_before_start_time"], 
                                                   end_time=eclipse_time_trio["one_day_before_end_time"], 
                                                   verbose=None)
                #f1, one_day_before_psd=scipy.signal.periodogram(one_day_before_wav, fs_odb)
                ax.psd(one_day_before_wav, Fs=fs_odb, color="blue", label="One Day Before")
                freqs_out_odb_wel, odb_wav_psd_welch=calc_psd(one_day_before_wav, fs_odb)
                freqs_out_odb_bart, odb_wav_psd_bart=calc_psd(one_day_before_wav, fs_odb, Bartlett=True)

                #Write write out file of data to be analyzed 
                odb_data_start_time=filename_2_datetime(one_day_before_files[0])[0].strftime("%Y-%B-%d_%H%M%S")+"_UTC".replace(" ", "")
                odb_data_start_time=one_day_before_str
                wav_file_name=os.path.join(wave_folder, 
                                           "ESID#"+ESID+"_"+odb_data_start_time+".WAV")
                wavfile.write(wav_file_name, fs_odb, one_day_before_wav)
            ###########################################################################
            #create the legend and the plots.  This indentation ensures that the plot will 
            # be made, even if there are only eclipse files 
            if old_plots:       
                legend = ax.legend(loc='upper center', shadow=True, fontsize='large')
                plt.savefig(plot_1_name)
                if verbose: print("Saved file "+plot_1_name)    
                plt.savefig(plot_1a_name)
                if verbose: print("Saved file "+plot_1a_name)
            plt.close(fig)
        ###########################################################################
        #Make Plots of the Welch PSD
        if type(freqs_out_ecl_wel) == type(test_arr):

            plt.figure()
            plt.title("PSD Welch's & Bartlett's Method "+ESID+" Eclipse on "+str(df["FirstContactDate"].values[0]))
            plt.semilogy(freqs_out_ecl_wel/to_kHz, eclipse_wav_psd_welch,color="orange", label="W. Eclipse Day")
            if type(freqs_out_odb_wel) == type(test_arr):
                 plt.semilogy(freqs_out_odb_wel/to_kHz, odb_wav_psd_welch/to_kHz, color="blue", label="W. One Day Before")
            if type(freqs_out_tdb_wel) == type(test_arr):
                 plt.semilogy(freqs_out_tdb_wel/to_kHz, tdb_wav_psd_welch/to_kHz, color="green", label="W. Two Days Before")
            ###########################################################################
            #create the legend and the plots.  This indentation ensures that the plot will 
            # be made, even if there are only eclipse files
            #plt.xlabel('frequency [Hz]')
            #plt.ylabel('PSD [V**2/Hz]')
            #plt.legend(loc='upper center', shadow=True, fontsize='large')

            #plt.savefig(plot_2a_name)
            #if verbose: print("Saved file "+plot_2a_name)
            #plt.close(fig)
        ##########################################################################    
        #Make Plots of the Bartlett PSD
        if type(freqs_out_ecl_bart) == type(test_arr) and old_plots:
            #plt.figure()
            #plt.title("PSD Bartlett's Method "+ESID+" Eclipse on "+str(df["FirstContactDate"].values[0]))
            plt.scatter(freqs_out_ecl_bart/to_kHz, eclipse_wav_psd_bart*to_kHz,color="orange", 
                        label="B. Eclipse Day", marker='D')  # 'D' specifies diamond shape
            if type(freqs_out_odb_bart) == type(test_arr):
                 plt.scatter(freqs_out_odb_bart/to_kHz, odb_wav_psd_bart/to_kHz, color="blue", 
                             label="B. One Day Before", marker='D')  # 'D' specifies diamond shape
            if type(freqs_out_tdb_bart) == type(test_arr):
                 plt.scatter(freqs_out_tdb_bart/to_kHz, tdb_wav_psd_bart/to_kHz, color="green", 
                             label="B. Two Days Before", marker='D')  # 'D' specifies diamond shape
            ###########################################################################
            #create the legend and the plots.  This indentation ensures that the plot will 
            # be made, even if there are only eclipse files
            plt.xlabel(x_axis_freq_label)
            plt.ylabel(y_axis_freq_label)
            plt.legend(loc='upper center', shadow=True, fontsize='large')
            
            #plt.savefig(plot_2b_name)
            #if verbose: print("Saved file "+plot_2b_name)
            if old_plots:
                plt.savefig(plot_2a_name)
                if verbose: print("Saved file "+plot_2a_name)
            plt.close(fig)

        ###########################################################################
        #Calculate and plot the Average PSD on non-eclipse days with error bars
        #You need both one day before data and two day before data to calculate this.
        #Need to test against an array because the truth value of an array with more 
        # than one element is ambiguous. 
        if type(freqs_out_odb_bart) == type(test_arr) and type(freqs_out_tdb_bart) == type(test_arr) :
            interp_freqs, avg_psd, avg_psd_std=compute_average_and_std(
                 freqs_out_odb_wel, odb_wav_psd_welch, 
                 freqs_out_tdb_wel, tdb_wav_psd_welch)
            # Plot the with error bars


                 
            # Calculate twice the standard error
            twice_standard_error = 2.0 * avg_psd_std

            plt.figure()
            plt.title("Eclipse PSD and Avg PSD"+ESID+" Eclipse on "+str(df["FirstContactDate"].values[0]))
            # Plot the average with standard deviation error bars

            # Overplot twice the standard error
            plt.errorbar(interp_freqs/to_kHz, avg_psd*to_kHz, yerr=twice_standard_error*to_kHz, fmt='o', label='Twice Standard Error',
                         color='green', ecolor='blue', elinewidth=2, capsize=4,alpha=0.7)
            
            # Overplot  the standard error
            plt.errorbar(interp_freqs/to_kHz, avg_psd*to_kHz, yerr=avg_psd_std*to_kHz, fmt='o', label='Average with Std Dev',
                         color='green', ecolor='green', elinewidth=2, capsize=4, alpha=0.5)
            
            # Overlay the eclipse day data (freqs_out_ecl_wel, eclipse_wav_psd_welch) with a different style
            plt.plot(freqs_out_ecl_wel/to_kHz, eclipse_wav_psd_welch*to_kHz, label='Eclipse Day', 
                     color='orange', linewidth=2.5, linestyle='solid')
            
            # Set the y-axis to semilog scale
            plt.yscale('log')
            plt.xlabel(x_axis_freq_label)
            plt.ylabel(y_axis_freq_label)
            plt.legend(loc='upper center', shadow=True, fontsize='large')
            if old_plots:
                plt.savefig(plot_3a_name)
                if verbose: print("Saved file "+plot_3a_name)
                plt.savefig(plot_3b_name)
            if verbose: print("Saved file "+plot_3b_name)
            plt.close(fig)
            ###########################################################################
            #Plot the Average PSD on non-eclipse days with error bars and the eclipse 
            # day PSD in the cricket frenquency range
            plt.figure()
            plt.title("Eclipse PSD and Avg PSD"+ESID+" Eclipse on "+str(df["FirstContactDate"].values[0]))
            # Plot the average with standard deviation error bars

            # Overplot twice the standard error
            plt.errorbar(interp_freqs/to_kHz, avg_psd*to_kHz, yerr=twice_standard_error*to_kHz, fmt='o', label='Twice Standard Error',
                         color='green', ecolor='blue', elinewidth=2, capsize=4,alpha=0.7)
            
            # Overplot  the standard error
            plt.errorbar(interp_freqs/to_kHz, avg_psd*to_kHz, yerr=avg_psd_std*to_kHz, fmt='o', label='Average with Std Dev',
                         color='green', ecolor='green', elinewidth=2, capsize=4, alpha=0.5)
            
            # Overlay the eclipse day data (freqs_out_ecl_wel, eclipse_wav_psd_welch) with a different style
            plt.plot(freqs_out_ecl_wel/to_kHz, eclipse_wav_psd_welch*to_kHz, label='Eclipse Day', 
                     color='orange', linewidth=2.5, linestyle='solid')
            
            # Set the y-axis to semilog scale
            #plt.yscale('log')
            #set the range for crickets [2 to 8 kHz]
            plt.xlim(cricket_freq_range[0]/to_kHz, cricket_freq_range[1]/to_kHz)
            # Use np.where to find the indices of elements between x1 and x2 (inclusive)
            indices1 = np.where((interp_freqs >= np.min(cricket_freq_range)) & (interp_freqs <= np.max(cricket_freq_range)))[0]
            indices2 = np.where((freqs_out_ecl_wel >= np.min(cricket_freq_range)) & (freqs_out_ecl_wel <= np.max(cricket_freq_range)))[0]
            ymin=.98*np.min([np.min(eclipse_wav_psd_welch[indices2]),
                             np.min(avg_psd[indices1]-twice_standard_error[indices1])])*to_kHz
            ymax=1.02*np.max([np.max(eclipse_wav_psd_welch[indices2]),
                         np.max(avg_psd[indices1]+twice_standard_error[indices1])])*to_kHz
            plt.ylim(ymin, ymax)
            plt.xlabel(x_axis_freq_label)
            plt.ylabel(y_axis_freq_label)
            plt.legend(loc='upper center', shadow=True, fontsize='large')
            if old_plots:
                plt.savefig(plot_4a_name)
                if verbose: print("Saved file "+plot_4a_name)
                plt.savefig(plot_4b_name)
                if verbose: print("Saved file "+plot_4b_name)
            plt.close(fig)
            ###########################################################################
            #Calculate and plot the Relative PSD in the cricket frenquency range
            #relative_psd()
            # Interpolate y-values to the interp_freqs values
            interp_eclipse_day_psd=np.interp(
                interp_freqs, freqs_out_ecl_wel, eclipse_wav_psd_welch,
                left=eclipse_wav_psd_welch[0],
                right=eclipse_wav_psd_welch[-1])
             # Use np.where to find the indices of elements between x1 and x2 (inclusive)
            indices1 = np.where(
                (interp_freqs >= np.min(cricket_freq_range)) 
                & (interp_freqs <= np.max(cricket_freq_range))
                )[0]
            
            
            relative_error=avg_psd_std/avg_psd
            relative_2_times_error=twice_standard_error/avg_psd

            relative_psd=interp_eclipse_day_psd/avg_psd

            one_line=np.ones(len(relative_psd))

            plt.figure()
            plt.title("Relative PSD"+ESID+" Eclipse on "+str(df["FirstContactDate"].values[0]))
            #Plot a line showing all ones.
            plt.plot(interp_freqs[indices1]/to_kHz, one_line[indices1], color='gray', linestyle=':')

            # Plot the average with standard deviation error bars

            # Overplot twice the standard error
            plt.errorbar(interp_freqs[indices1]/to_kHz, one_line[indices1], 
                         yerr=relative_2_times_error[indices1], fmt='o', 
                         label='Relative Standard Error x 1, & x 2',
                         color='blue', ecolor='blue', elinewidth=2, 
                         capsize=4.5,alpha=0.7
                         )
            
            # Overplot  the standard error
            plt.errorbar(interp_freqs[indices1]/to_kHz, one_line[indices1], 
                         yerr=relative_error[indices1], fmt='o', 
                         #label='One Standard Error',
                         color='blue', ecolor='blue', elinewidth=2, 
                         capsize=4,alpha=0.7
                         )
            
            # Overlay the eclipse day data  with a different style
            plt.plot(interp_freqs[indices1]/to_kHz, relative_psd[indices1], 
                     label='Eclipse Day Power Spectral Density \nRelative to the Average', 
                     color='orange', linewidth=2.5, linestyle='solid'
                     )
            
            # Set the y-axis to semilog scale
            #plt.yscale('log')
            #set the range for crickets [2 to 8 kHz]
            plt.xlim(cricket_freq_range[0]/to_kHz, cricket_freq_range[1]/to_kHz)
           
            ymin=.98*np.min(relative_psd[indices1])
            ymax=1.05*np.max(relative_psd[indices1])
            ymin=-0.1

            plt.ylim(ymin, ymax)
            plt.xlabel(x_axis_freq_label)
            plt.ylabel("Relative Power Spectral Density")
            plt.legend(loc='upper center', shadow=True, fontsize='large')
            if old_plots:
                plt.savefig(plot_5a_name)
                if verbose: print("Saved file "+plot_5a_name)
            plt.close(fig)

            if os.path.isfile(relative_psd_csv) and old_plots:
                relative_psd_df=pd.DataFrame(
                    {"Frequencies [kiloHertz]":interp_freqs[indices1]/to_kHz,
                     "Relative Power Spectral Density Change": relative_psd[indices1],
                     "Relative Error": relative_error[indices1],
                     "Relative Error x 2":relative_2_times_error[indices1]
                     }
                     )
                relative_psd_df.to_csv(relative_psd_csv, index=False)

            else:
                if relative_psd_csv:
                    print(relative_psd_csv+ " is not a valid file location.")
                else:
                    if verbose: print("No Relative PSD csv filename given.")


            ###########################################################################
            #Calculate cricket frequency values
            indices1 = np.where((freqs_out_odb_wel >= np.min(cricket_freq_range)) & (freqs_out_odb_wel <= np.max(cricket_freq_range)))[0]
            indices2 = np.where((freqs_out_tdb_wel >= np.min(cricket_freq_range)) & (freqs_out_tdb_wel <= np.max(cricket_freq_range)))[0]
            indices3 = np.where((freqs_out_ecl_wel >= np.min(cricket_freq_range)) & (freqs_out_ecl_wel <= np.max(cricket_freq_range)))[0]

            integrated_psd_odb = np.trapz(odb_wav_psd_welch[indices1], 
                                          freqs_out_odb_wel[indices1])
            integrated_psd_tdb = np.trapz(tdb_wav_psd_welch[indices2], 
                                          freqs_out_tdb_wel[indices2])
            
            # Calculate the average and standard deviation
            average_V2 = (integrated_psd_odb + integrated_psd_tdb) / 2.0
            V2_std = np.std([integrated_psd_odb, integrated_psd_tdb], axis=0)

            integrated_psd_ecl = np.trapz(eclipse_wav_psd_welch[indices3], 
                                          freqs_out_ecl_wel[indices3])
            
            diff=integrated_psd_ecl-average_V2
            std_dev_diff=diff/V2_std
            
            ###########################################################################
            #Calculate all frequency values
            integrated_psd_odb_all = np.trapz(odb_wav_psd_welch, 
                                          freqs_out_odb_wel)
            integrated_psd_tdb_all = np.trapz(tdb_wav_psd_welch, 
                                          freqs_out_tdb_wel)
            
            # Calculate the average and standard deviation
            average_V2_all = (integrated_psd_odb_all + integrated_psd_tdb_all) / 2.0
            V2_std_all = np.std([integrated_psd_odb_all, integrated_psd_tdb_all], axis=0)

            integrated_psd_ecl_all = np.trapz(eclipse_wav_psd_welch, 
                                          freqs_out_ecl_wel)
            
            diff_all=integrated_psd_ecl_all-average_V2_all
            std_dev_diff_all=diff_all/V2_std_all
            ###########################################################################
            #Calculate the relative power as a function of time.
            two_days_before_times, two_days_before_power = power_in_frequency_range_welch(
                fs_tdb, 
                two_days_before_wav,
                cricket_freq_range
                )
            one_day_before_times, one_day_before_power = power_in_frequency_range_welch(
                fs_odb, 
                one_day_before_wav,
                cricket_freq_range
                )
            eclipse_times, eclipse_power = power_in_frequency_range_welch(
                fs_ecl, 
                eclipse_wav,
                cricket_freq_range
                )

            avg_times,avg_power,avg_power_std = compute_average_and_std(two_days_before_times, 
                                                                        two_days_before_power, 
                                                                        one_day_before_times, 
                                                                        one_day_before_power)
            
            if np.min(avg_power) < 0.0 or  np.min(avg_power_std) < 0.0:
                if np.min(avg_power) < 0.0:
                    print("np.min(avg_power) < 0 at site ")
                    print("# of negative indices in avg_power: ",len(avg_power[np.where(np.any(avg_power<=0))]))
                    print("Negative indices in avg_power: ", np.where(np.any(avg_power<=0)))
                if np.min(avg_power_std):
                    print("np.min(avg_power_std) < 0 at site ")
                    print("# of negative indices in avg_power_std: ",len(avg_power_std[np.where(np.any(avg_power_std<=0))]))
                    print("Negative indices in avg_power: ", np.where(np.any(avg_power_std<=0)))
                
                if np.min(one_day_before_power):
                    print("np.min(one_day_before_power) < 0 at site ")
                    print("# of negative indices in one_day_before_power: ",len(one_day_before_power[np.where(np.any(one_day_before_power<=0))]))
                    print("Negative indices in one_day_before_power: ", np.where(np.any(one_day_before_power<=0)))
                if np.min(two_days_before_power):
                    print("np.min(two_days_before_power) < 0 at site ")
                    print("# of negative indices in two_days_before_power: ",len(two_days_before_power[np.where(np.any(two_days_before_power<=0))]))
                    print("Negative indices in two_days_before_power: ", np.where(np.any(two_days_before_power<=0)))
                print("Check file "+plot_5a_name)

            # Interpolate eclipse day power to match the avg_times
            eclipse_day_power=np.interp(
                avg_times, eclipse_times, eclipse_power,
                left=eclipse_power[0],
                right=eclipse_power[len(eclipse_power)-1]
                )
            
            if np.min(eclipse_day_power) < 0.0:
                print("np.min(eclipse_day_power) < 0 at site ")
                print("# of negative indices in eclipse_day_power: ",len(eclipse_day_power[np.where(np.any(eclipse_day_power <=0))]))
                print("Negative indices in eclipse_day_power: ",np.where(np.any(eclipse_day_power <=0)))

                eclipse_day_power[np.where(eclipse_day_power<=0)]=np.min(eclipse_day_power)
            #Percent (relative error)
            relative_power_error=avg_power_std/avg_power

            #Eclipse relative power
            eclipse_relative_power=eclipse_day_power/avg_power

            one_line=np.ones(len(avg_times))
            Rel_power_title= "Relative Power on Eclipse Day \nRelative to Two Non-Eclipse Days in Cricket Freqencies \nat site ESID#"+ESID+" Eclipse on "+str(df["FirstContactDate"].values[0])
            #Rel_power_title_temp=[]
            #counter=0
            #for  i in range(500):
            #    Rel_power_title_temp.append(str(500-i))
            
            #Rel_power_title=""
            
            #for element in Rel_power_title_temp:
            #    Rel_power_title=Rel_power_title+element+","

            plt.figure()
            plt.title(Rel_power_title)
            #Plot a line showing all ones.
            plt.plot(avg_times, one_line, color='gray', linestyle=':')

            # Plot the average with standard deviation error bars

            # Overplot twice the standard error
            plt.errorbar(avg_times, one_line, 
                         yerr=2.0*relative_power_error, fmt='o', 
                         label='One Relative Standard Error',
                         color='blue', ecolor='blue', elinewidth=2, 
                         capsize=4.5,alpha=0.7
                         )
            
            # Overplot  the standard error
            plt.errorbar(avg_times, one_line, 
                         yerr=relative_power_error, fmt='o', 
                         #label='One Standard Error',
                         color='blue', ecolor='blue', elinewidth=2, 
                         capsize=4,alpha=0.7
                         )
            
            # Overlay the eclipse day data  with a different style
            plt.plot(avg_times, eclipse_relative_power, 
                     label='Eclipse Day Power \nin Cricket Frequencies \nRelative to the Average Power of Two Non-Eclipse Days', 
                     color='orange', linestyle='solid',
                     )
            #Plot a line showing all ones.
            plt.plot(avg_times, one_line, color='gray',  linewidth=3, linestyle=':',
                     label="Relative Average Power of Two Non-Eclipse Days")

            # Set the y-axis to semilog scale
            #plt.yscale('log')
            #set the range for crickets [2 to 8 kHz]
            #plt.xlim(cricket_freq_range[0]/to_kHz, cricket_freq_range[1]/to_kHz)
           
            ymin=-0.01
            ymax=1.8*max([np.max(1.0+relative_power_error),np.max(eclipse_relative_power)])
            plt.ylim(ymin, ymax)
            plt.xlabel(
                "Seconds From Eclipse Start Time at: "+ \
                    str(df["FirstContactDate"].values[0])+ " "+ \
                    str(df["MaxEclipseTimeUTC"].values[0])+ " "+ \
                    "UTC" 
                )
            plt.ylabel("Relative Power")
            plt.legend(loc='upper center', shadow=True, 
                       fontsize='small',
                       fancybox=True)
            if old_plots:
                plt.savefig(plot_6a_name)
                if verbose: print("Saved file "+plot_6a_name)
            plt.close(fig)
            ###########################################################################
            #Output relative power as a function of time to a csv file.
            df_rel_power=pd.DataFrame({
                "Seconds From Eclipse Start Time at: \n"+ \
                    str(df["FirstContactDate"].values[0])+ " \n"+ \
                        str(df["MaxEclipseTimeUTC"].values[0])+ " \n"+ \
                            "UTC":avg_times,
                "Eclipse Day Power in Cricket Frequencies \nRelative to the Average Power of Two Non-Eclipse Days":eclipse_relative_power,
                "One Relative Standard Error":relative_power_error,
                "Two Relative Standard Errors":2.0*relative_power_error
                }
                )
            if old_plots:
                df_rel_power.to_csv(csv_6a_name, index=False)

            ###########################################################################
            # Create the site spreadsheet
            if spreadsheets_folder:
                if verbose: print(spreadsheets_folder)
                interp_tdb_day_psd=np.interp(
                    interp_freqs, freqs_out_tdb_wel, freqs_out_tdb_wel,
                    left=freqs_out_tdb_wel[0],
                    right=freqs_out_tdb_wel[-1])
            
                interp_odb_day_psd=np.interp(
                    interp_freqs, freqs_out_odb_wel, odb_wav_psd_welch,
                    left=odb_wav_psd_welch[0],
                    right=odb_wav_psd_welch[-1])
                            
                spread_freqs=interp_freqs[indices1]
                eclipse_rel_psd=interp_eclipse_day_psd[indices1]/avg_psd[indices1]
                
                cricket_avg_psd_std=avg_psd_std[indices1]
                cricket_avg_psd=avg_psd[indices1]
                cricket_rel_avg_psd=avg_psd[indices1]/avg_psd[indices1]
                cricket_rel_avg_psd_std=avg_psd_std[indices1] / avg_psd[indices1]    

                if verbose:
                    print("Length of interp_eclipse_day_psd " +
                          str(len(interp_eclipse_day_psd[indices1]))
                          )
                    print("Length of avg_psd[indices1] " +
                          str(len(avg_psd[indices1]))
                          )
                    print("Length of cricket_avg_psd_std " +
                          str(len(cricket_avg_psd_std))
                          )
                    print("Length of eclipse_rel_psd " +
                          str(len(eclipse_rel_psd))
                          )



                number_of_stds=eclipse_rel_psd/cricket_rel_avg_psd_std

                max_num_of_stds=[]
                gt_2_stds=[]
                max_stds=np.max(np.absolute(number_of_stds))
                 
                significant="N"
                
                print(max_stds)
                m2=max_stds
                print(m2)
                
                counter=0
                for element in number_of_stds:
                    if np.absolute(element) >= max_stds:
                        temp1="Y"
                        max_freq=spread_freqs[counter]/to_kHz
                        rel_psd_max=eclipse_rel_psd[counter]
                        max_rel_error=cricket_rel_avg_psd_std[counter]
                        
                    else: temp1="N"
                    max_num_of_stds.append(temp1)
                    if np.absolute(element) >= 2.0:
                        temp2="Y"
                        significant="Y"
                    else: 
                        temp2="N"
                    gt_2_stds.append(temp2)
                    counter+=1 


                current_time = datetime.datetime.now()
                # Format the current time as YYYY_MM_DD_hh_mm
                formatted_time = current_time.strftime("%Y_%m_%d_%H_%M")

                site_spreadsheet_name=os.path.join(spreadsheets_folder, 
                                                   formatted_time+"_ESID#"+ESID+"_Relative_PSD_analysis.csv")
                
                mk_esid_site_psd_spreadsheet(spread_freqs/to_kHz, 
                                             interp_tdb_day_psd[indices1]/to_kHz, 
                                             interp_odb_day_psd[indices1]/to_kHz,
                                             cricket_avg_psd,   
                                             cricket_avg_psd_std,
                                             cricket_rel_avg_psd_std, 
                                             interp_eclipse_day_psd[indices1],  
                                             eclipse_rel_psd,
                                             number_of_stds,
                                             max_num_of_stds, 
                                             gt_2_stds,
                                             outname=site_spreadsheet_name, 
                                             Dictionary=False
                                             )
            
            ###########################################################################
            # Create or add to the relative_psd_master_analysis spreadsheet
            if relative_psd_csv:
                
                mk_relative_psd_master_analysis(ESID, 
                                                second_contact, 
                                                third_contact,
                                                eclipse_local_type, 
                                                rel_psd_max,
                                                max_freq,
                                                max_rel_error,
                                                max_stds,
                                                significant,
                                                m2,
                                                outname=new_relative_psd_csv, 
                                                Dictionary=False)
            ###########################################################################
            # Create the relative psd plot
            if plot_5a_name:
                
                mk_rel_psd_plot(ESID, 
                                second_contact,
                                freqs_out_tdb_wel, 
                                tdb_wav_psd_welch,
                                freqs_out_odb_wel, 
                                odb_wav_psd_welch, 
                                freqs_out_ecl_wel, 
                                eclipse_wav_psd_welch,
                                cricket_freq_range, 
                                plot_main_title=False,
                                outname=plot_5a_name,
                                verbose=verbose)  
            ###########################################################################
            # Create the output text
            out_text=str(ESID).zfill(3)+"," #"ESID,"
            out_text=out_text+str(integrated_psd_odb_all)+"," #"All Frequencies: 4/6/2024 Pascals^2,
            out_text=out_text+str(integrated_psd_tdb_all)+"," #All Frequencies: 4/7/2024 Pascals^2,"
            out_text=out_text+str(average_V2_all)+"," #"All Frequencies: Average Pascals^2 of 4/6 & 4/7,"
            out_text=out_text+str(V2_std_all)+"," #"All Frequencies: Standard Deviation 4/6 & 4/7,"
            out_text=out_text+str(integrated_psd_ecl_all)+"," #"All Frequencies: Eclipse 4/8/2024 Pascals^2,"	
            out_text=out_text+str(std_dev_diff_all)+"," #"All Frequencies: Standard Deviation difference (Eclipse vs Average),"
            out_text=out_text+str(integrated_psd_tdb)+"," #"Cricket Frequencies: 4/6/2024 PSD,"
            out_text=out_text+str(integrated_psd_odb)+"," #"Cricket Frequencies: 4/7/2024 PSD,"
            out_text=out_text+str(average_V2)+"," #"Cricket Frequencies: Average Pascals^2 of 4/6 & 4/7,"
            out_text=out_text+str(V2_std)+"," #"Cricket Frequencies: Standard Deviation 4/6 & 4/7,"
            out_text=out_text+str(integrated_psd_ecl)+"," #"Cricket Frequencies: Eclipse 4/8/2024 Pascals^2," 
            out_text=out_text+str(std_dev_diff)#"Cricket Frequencies: Standard Deviation difference (Eclipse vs Average)") 
            #out_text=out_text+
            out_text=out_text+"\n"                  
    ###########################################################################
    #Can't do anything if there is no eclipse_data_csv file
    else:
        print("No file "+eclipse_data_csv+" found.")
        out_text=str(ESID).zfill(3)+",,,,,,,,,,,,"+"\n"
       
    return out_text

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
    text=text+"Latitude: "+ str(eclipse_info["Latitude"]) +"\n"
    text=text+"Longitude: "+ str(eclipse_info["Longitude"])  +"\n"
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
 
       

        if eclipse_data_csv : 
            eclipse_data_csv=eclipse_data_csv[0]
            #time_format="%Y-%m-%d %H:%M:%S"
            eclipse_info=escsp_read_eclipse_csv(eclipse_data_csv, verbose=verbose, ESID=ESID)


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
            eclipse_year=str(eclipse_time_trio["eclipse_start_time"].year)
            eclipse_start_str=eclipse_time_trio["eclipse_start_time"].strftime("%Y-%B-%d_%H%M%S")+"UTC".replace(" ", "")
            one_day_before_str=eclipse_time_trio["one_day_before_start_time"].strftime("%Y-%B-%d_%H%M%S")+"UTC".replace(" ", "")
            two_days_before_str=eclipse_time_trio["two_days_before_start_time"].strftime("%Y-%B-%d_%H%M%S")+"UTC".replace(" ", "")
            eclipse_date_str=eclipse_info["FirstContactDate"]
            
            if eclipse_files: 
                if verbose: print("youtube_folder= "+youtube_folder)
                clip_basename="ESID#"+str(ESID)+"_"+eclipse_year+"_"+eclipse_type+"_"+eclipse_start_str+"_eclipse"
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
                clip_basename="ESID#"+str(ESID)+"_"+eclipse_year+"_"+eclipse_type+"_"+two_days_before_str+"_two_days_before"
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
                clip_basename="ESID#"+str(ESID)+"_"+eclipse_year+"_"+eclipse_type+"_"+one_day_before_str+"_one_day_before"
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
         site_values[columns[1]]=0

    #Get size of data in the folder in GB str(round(answer, 2))
    site_values[columns[2]]=str(round(get_folder_size_in_gb(folder),2))
    
    if site_values[columns[1]] == 1: 
         if AM_timestamp_set(folder) == True:
            site_values[columns[3]]=1
            
            site_values[columns[4]]=0
            if times_between_dates(folder, dates[2], dates[3]):
                site_values[columns[5]]=1
            else:
                site_values[columns[5]]=0
              
            if times_between_dates(folder, dates[4], dates[5]):
                site_values[columns[6]]=1
            else:
                site_values[columns[6]]=0

            if times_between_dates(folder, dates[6], dates[7]):
                site_values[columns[7]]=1
            else:
                site_values[columns[7]]=0

            if times_between_dates(folder, dates[8], dates[9]):
                site_values[columns[8]]=1
            else:
                site_values[columns[8]]=0

            if times_between_dates(folder, dates[10], dates[11]): 
                site_values[columns[9]]=1
            else:
                site_values[columns[9]]=0

            if site_values[columns[5]] == 1 and site_values[columns[6]] == 1 and site_values[columns[7]] == 1:
              site_values[columns[4]]=1
            else:
              site_values[columns[4]]=0
            
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

def calc_psd(input, fs_in, Bartlett=False):
    """
    Calcute the power spectral density of an array or the contents of a wav file

    Parameters:
    input (str or array): If input is a string then the code will assume that it is a path to a .WAV file.  
                            If not the code will generate an error. [Not yet implemented]
                        If input is an array then the code will interpret it as the data array from a .WAV file.

    fs (float): The path to the folder.
    Bartlett (any): If Bartlett != False then noverlap=0 which will compute the PSD using Bartlett's method. 
                    Default is False which uses Welch's method. 
    
    Returns:
    freqs_out (array): Array of Frequencies
    Pxx_den   (array): Power Spectral density as a function of frequency. [V**2/Hz]
    """

    if Bartlett:
         noverlap=0
    else: noverlap=None

    freqs_out, Pxx_den=scipy.signal.welch(
          input,                #Data array read in from .WAV file
          fs=fs_in,         #Frequency sampling  read in from .WAV file
          window='hann',	#Use a Hann window for filtering. Default 
          nperseg=None, 	#Length of each segment.  None allows the default
          noverlap=noverlap,    # None sets the number of overlapping points to noverlap = 
                            #nperseg // 2  
          nfft=None,		#If None, the FFT length is nperseg. Default
          detrend='constant',	#Default
          return_onesided=True,	#If True, return a one-sided spectrum for real data. No 
                                #complex components.
          scaling='density', 	#Set to power spectral density Pxx[V**2/Hz] instead of the
                                #squared magnitude spectrum Pxx[V**2]           
          axis=-1,          #Axis along which the periodogram is computed; the default is 
                            #over the last axis (i.e. axis=-1).
          average='mean'    #Method to use when averaging periodograms.  Default.
          )
    
    return freqs_out, Pxx_den

def compute_average_and_std(x1, y1, x2, y2):
    """
    Compute the average and standard deviation of y-values for given x1, y1, x2, y2 arrays.
    
    Args:
    - x1, y1 (array-like): x and y values of the first dataset.
    - x2, y2 (array-like): x and y values of the second dataset.
    
    Returns:
    - x_avg (numpy array): Common x values.
    - y_avg (numpy array): Average y values at x3.
    - y_std (numpy array): Standard deviation of y values at x3.
    """
    # Find common x values using a union of x1 and x2
    x_avg = np.union1d(x1, x2)

    # Interpolate y-values for both datasets onto the common x3 values
    interp_y1 = interp1d(x1, y1, 
                         kind='linear', fill_value=(y1[0],y1[-1]),
                         bounds_error=False)
    #fill_value='extrapolate')
    interp_y2 = interp1d(x2, y2, 
                         kind='linear', fill_value=(y2[0],y2[-1]),
                         bounds_error=False)
    #fill_value='extrapolate')
    
    y1_interp = interp_y1(x_avg)
    y2_interp = interp_y2(x_avg)
    
    # Calculate the average and standard deviation
    y_avg = (y1_interp + y2_interp) / 2
    y_std = np.std([y1_interp, y2_interp], axis=0)
    
    return x_avg, y_avg, y_std

def compute_average_and_std_3_arrays(x1, y1, x2, y2, x3, y3):
    """
    Compute the average and standard deviation of y-values for given x1, y1, x2, y2, x3, y3 arrays.
    
    Args:
    - x1, y1 (array-like): x and y values of the first dataset.
    - x2, y2 (array-like): x and y values of the second dataset.
    - x3, y3 (array-like): x and y values of the third dataset.
    
    Returns:
    - x_avg (numpy array): Common x values.
    - y_avg (numpy array): Average y values at x_avg.
    - y_std (numpy array): Standard deviation of y values at x_avg.
    """
    # Find common x values using a union of x1, x2, and x3
    x_avg = np.union1d(np.union1d(x1, x2), x3)

    # Interpolate y-values for all three datasets onto the common x_avg values
    interp_y1 = interp1d(x1, y1, kind='linear', fill_value=(y1[0],y1[-1]))#fill_value='extrapolate')
    interp_y2 = interp1d(x2, y2, kind='linear', fill_value=(y1[0],y1[-1]))#fill_value='extrapolate')
    interp_y3 = interp1d(x3, y3, kind='linear', fill_value=(y1[0],y1[-1]))#fill_value='extrapolate')
    
    y1_interp = interp_y1(x_avg)
    y2_interp = interp_y2(x_avg)
    y3_interp = interp_y3(x_avg)
    
    # Calculate the average and standard deviation
    y_avg = (y1_interp + y2_interp + y3_interp) / 3
    y_std = np.std([y1_interp, y2_interp, y3_interp], axis=0)
    
    return x_avg, y_avg, y_std

def extract_row_by_esid(csv_file, esid_string=False , verbose=False):
    """
    Extracts the row from a CSV file where the 'AudioMoth ES ID Number' matches a given string.
    
    Args:
    - csv_file (str): Path to the CSV file.
    - esid_string (str): The ESID string to match.
    
    Returns:
    - pd.DataFrame: A DataFrame containing the matching row(s), or False if no match is found.
    """
    matching_row=None

    if verbose: 
        print("csv file= "+csv_file)
    if type(esid_string) != type('a'):
        print("esid_string was not a string attempting to fix.")
        print("esid_string was= "+str(esid_string)+", "+type(esid_string).__name__)
        esid_string=str(esid_string).zfill(3)
        print("esid_string now= "+esid_string)
    else: 
        print("ESID#= "+esid_string)
    if esid_string.lower() != "none":
    # Read the CSV file into a DataFrame
        if os.path.isfile(csv_file) and esid_string != False and esid_string != None:
            df = pd.read_csv(csv_file)
            if type(df).__name__ == 'DataFrame':
                if verbose: 
                    print("Type df= "+str(type(df)))
                    print(df.columns)
                    print(esid_string)
    # Search for rows where 'AudioMoth ES ID Number' matches the input string
                if (df['AudioMoth ES ID Number'].values == esid_string).any() :
                    matching_row = df.loc[df['AudioMoth ES ID Number'].values == esid_string]
            #matching_row = df[df['AudioMoth ES ID Number'].values[0] == esid_string]
                else:
                    if (df['AudioMoth ES ID Number'].values == int(esid_string)).any(): 
                        matching_row = df.loc[df['AudioMoth ES ID Number'].values == int(esid_string)]
            #matching_row = df[df['AudioMoth ES ID Number'].values[0] == int(esid_string)]
            
            else:
                print("Type df= "+str(type(df)))
                print("No Matching ESID found for "+str(esid_string)+" in extract_row_by_esid.")

        print("not a valid esid: "+str(esid_string)+".")
            
    
    return matching_row

def Reports_2(folder, eclipse_data_csv=None, TOTAL=True, verbose=False, save=False):

    ESID=filename_2_ESID(folder)

    # Define the column headings
    if TOTAL:
        columns = [
             "ESID #", 
             "Config file Present = No, 1 = yes",
             "GB of data", 
             "AM Timestamp Set",
             "Eclipse Type",
             "Three Days of Data Recorded? @ eclipse time (Two days before and Eclipse Day 0 = No, 1 = yes)",
             "April 6, 2024 Data @ eclipse time (0 = No, 1 = yes)",
             "April 7, 2024 Data @ eclipse time (0 = No, 1 = yes)",
             "April 8, 2024 Data @ eclipse time (0 = No, 1 = yes)", 
             "April 9, 2024 Data @ eclipse time (0 = No, 1 = yes)",
             "April 10, 2024 Data  @ eclipse time (0 = No, 1 = yes)", 
             "April 11, 2024 Data  @ eclipse time (0 = No, 1 = yes)"
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
             "Eclipse Type",
             "Three Days of Data Recorded? @ eclipse time (Two days before and Eclipse Day 0 = No, 1 = yes)",
             "October 12, 2023 Data @ eclipse time (0 = No, 1 = yes)",
             "October 13, 2023 Data @ eclipse time (0 = No, 1 = yes)",
             "October 14, 2023 Data  @ eclipse time (0 = No, 1 = yes)", 
             "October 15, 2023 Data  @ eclipse time (0 = No, 1 = yes)",
             "October 16, 2023 Data  @ eclipse time (0 = No, 1 = yes)", 
             "October 17, 2023 Data  @ eclipse time (0 = No, 1 = yes)"
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
         site_values[columns[1]]=0

    #Get size of data in the folder in GB str(round(answer, 2))
    site_values[columns[2]]=str(round(get_folder_size_in_gb(folder),2))
   
    #"Eclipse Type"
    eclipse_info=escsp_read_eclipse_csv(eclipse_data_csv, ESID=ESID, verbose=verbose)
    if eclipse_info:
        site_values[columns[4]]=str(eclipse_info['Eclipse_type'])
    else:
        site_values[columns[4]]="not found"

    good_eclipse_type=True

    if not eclipse_info:
        good_eclipse_type=False
    else:
        
        if str(eclipse_info['Eclipse_type']).lower != "nan":
            good_eclipse_type=False
        if str(eclipse_info['Eclipse_type']).lower != "not found":
            good_eclipse_type=False


    if site_values[columns[1]] == 1 and  good_eclipse_type : 
         
        if AM_timestamp_set(folder) == True:
            site_values[columns[3]]=1

            data_check=does_eclipse_data_exist(folder, eclipse_data_csv=eclipse_data_csv, verbose=verbose)
            if data_check:
                #Two Days before
                if data_check["two_days_before"]:
                   site_values[columns[6]]=1
                else:
                    site_values[columns[6]]=0
                #One Day before  
                if data_check["one_day_before"]:
                    site_values[columns[7]]=1
                else:
                    site_values[columns[7]]=0
                #Eclipse Day
                if data_check["eclipse_day"]:
                    site_values[columns[8]]=1
                else:
                    site_values[columns[8]]=0
                #One Day after Eclipse
                if data_check["one_day_after"]:
                    site_values[columns[9]]=1
                else:
                    site_values[columns[9]]=0
                #Two Days after Eclipse
                if data_check["two_days_after"]: 
                    site_values[columns[10]]=1
                else:
                    site_values[columns[10]]=0

                if site_values[columns[6]] == 1 and site_values[columns[6]] == 1 and site_values[columns[7]] == 1:
                    site_values[columns[5]]=1
                else:
                    site_values[columns[5]]=0

            else:
                #Two Days before
                site_values[columns[6]]="N/A"
                #One Day before  
                site_values[columns[7]]="N/A"
                #Eclipse Day
                site_values[columns[8]]="N/A"
                #One Day after Eclipse
                site_values[columns[8]]="N/A"
                #Two Days after Eclipse
                site_values[columns[10]]="N/A"
                #Three days if recording
                site_values[columns[5]]="N/A"
            
        else:
            site_values[columns[4]]=0
            site_values[columns[5]] ="N/A"
            site_values[columns[6]] ="N/A"
            site_values[columns[7]] ="N/A"
            site_values[columns[5]] ="N/A"
            site_values[columns[9]] ="N/A"
            site_values[columns[10]] ="N/A"
    

         
    else:
        site_values[columns[3]] ="No Data"
        site_values[columns[4]] =" - "
        site_values[columns[5]] =" - "
        site_values[columns[6]] =" - "
        site_values[columns[7]] =" - "
        site_values[columns[8]] =" - "
        site_values[columns[9]] =" - "

    #return site_values
    df=pd.DataFrame.from_dict([site_values])

    # Define the output CSV file path
    output_file_path = os.path.join(folder,'Report_1.csv')

    #Save the DataFrame to a CSV file
    if save:
         df.to_csv(output_file_path, index=False)

    if verbose: print(f"DataFrame saved to {output_file_path}")   

    return df 

def does_eclipse_data_exist(folder, eclipse_data_csv=None, verbose=None, UTC_max_diff_hours=None):
    if not UTC_max_diff_hours:
        UTC_max_diff_hours=1

    ESID=filename_2_ESID(folder)
    
    if eclipse_data_csv:
        if verbose: print("eclipse_data_csv"+eclipse_data_csv)
    else:
         print("No eclipse_data_csv passed to does_eclipse_data_exist")
    if os.path.isfile(eclipse_data_csv) :
        eclipse_info=escsp_read_eclipse_csv(eclipse_data_csv, ESID=ESID, verbose=verbose)
        if verbose: print(eclipse_info)
        df=pd.DataFrame(eclipse_info, index=[0])
        #df=pd.read_csv(eclipse_data_csv, header=[0])
        time_format="%Y-%m-%d %H:%M:%S"
        if verbose: print("success! " + eclipse_data_csv)     

        if df['Eclipse_type'].values[0] != np.nan:
            data_check_dict={
                "eclipse type": df['Eclipse_type'].values[0],
                "two_days_before":False,
                "one_day_before":False,
                "eclipse_day":False,
                "one_day_after":False,
                "two_days_after":False
            }
            test=True
            if type(df["SecondContactTimeUTC"].values[0]) != type("test"):
                test=False
            eclipse_local_type= df['Eclipse_type'].values[0]
            if eclipse_local_type == "NaN":
                test=False
            if eclipse_local_type != "Annular" or eclipse_local_type != "Total": 
                test=False
            if df["SecondContactTimeUTC"].values[0] == 0:
                test=False

           
            if test :
        #if eclipse_type == "Annular" or eclipse_type == "Total":
        ###########################################################################
            #set the eclipse start time
                chars_to_remove=["\"", "\'", "[", "]"]
                second_contact=str(df["FirstContactDate"].values[0]+" "+df["SecondContactTimeUTC"].values[0])
                for char_to_remove in chars_to_remove:
                    second_contact.replace(char_to_remove, '')
                print(second_contact)
        #eclipse_start_time = datetime.datetime(2023, 10, 14, 17, 34) 
                eclipse_start_time = datetime.datetime.strptime(second_contact, time_format)
        ########################################################################### 
            #set the eclipse end time
        #eclipse_end_time = datetime.datetime(2023, 10, 14, 17, 39)
                third_contact = str(df["FirstContactDate"].values[0]+" "+df["ThirdContactTimeUTC"].values[0])
            ###########################################################################
            #
                for char_to_remove in chars_to_remove:
                    third_contact.replace(char_to_remove, '')
                eclipse_end_time =  datetime.datetime.strptime(third_contact, time_format) 
            else:
                max_eclipse=datetime.datetime.strptime(
                    df["FirstContactDate"].values[0]+ " " + df["MaxEclipseTimeUTC"].values[0], time_format)
                eclipse_start_time=max_eclipse-datetime.timedelta(minutes=3)
                eclipse_end_time=max_eclipse+datetime.timedelta(minutes=3)
        ########################################################################### 
        #
            two_days_before_start_time=eclipse_start_time-datetime.timedelta(hours=48+UTC_max_diff_hours)
            two_days_before_end_time=eclipse_end_time-datetime.timedelta(hours=48+UTC_max_diff_hours)

            one_day_before_start_time=eclipse_start_time-datetime.timedelta(hours=24+UTC_max_diff_hours)   
            one_day_before_end_time=eclipse_end_time-datetime.timedelta(hours=24+UTC_max_diff_hours)

            one_day_after_start_time=eclipse_start_time+datetime.timedelta(hours=24+UTC_max_diff_hours)   
            one_day_after_end_time=eclipse_end_time+datetime.timedelta(hours=24+UTC_max_diff_hours)
        
            two_days_after_start_time=eclipse_start_time+datetime.timedelta(hours=48+UTC_max_diff_hours)
            two_days_after_end_time=eclipse_end_time+datetime.timedelta(hours=48+UTC_max_diff_hours)

        ###########################################################################  
        recording_files=glob.glob(os.path.join(folder,"*."+"WAV"))
        if verbose: print(len(recording_files))  
        #get a list of datetime objects associated with the .WAV files 
        file_date_times=filename_2_datetime(recording_files, file_type="AudioMoth", verbose=verbose)

        
        two_days_before_begin=False
        two_days_before_end=False
        one_day_before_begin=False
        one_day_before_end=False
        eclipse_day_begin=False
        eclipse_day_end=False
        one_day_after_begin=False
        one_day_after_end=False
        two_days_after_begin=False
        two_days_after_end=False

        for file_date_time in file_date_times:
        # Check if the datetime is before the start time and after the end time
            if file_date_time <= two_days_before_start_time:
                two_days_before_begin=True
            if file_date_time >= two_days_before_end_time:
                two_days_before_end=True

            if file_date_time <= one_day_before_start_time:
                one_day_before_begin=True
            if file_date_time >= one_day_before_end_time:
                one_day_before_end=True

            if file_date_time <= eclipse_start_time:
                eclipse_day_begin=True
            if file_date_time >= eclipse_end_time:
                eclipse_day_end=True

            if file_date_time <= one_day_after_start_time:
                one_day_after_begin=True
            if file_date_time >= one_day_after_end_time:
                one_day_after_end=True

            if file_date_time <= two_days_after_start_time:
                two_days_after_begin=True
            if file_date_time >= two_days_after_end_time:
                two_days_after_end=True
    

        if two_days_before_begin and two_days_before_end:
            data_check_dict["two_days_before"]=True

        if one_day_before_begin and one_day_before_end:
            data_check_dict["one_day_before"]=True

        if eclipse_day_begin and eclipse_day_end:
            data_check_dict["eclipse_day"]=True

        if one_day_after_begin and one_day_after_end:
            data_check_dict["one_day_after"]=True
            
        if two_days_after_begin and two_days_after_end:
            data_check_dict["two_days_after"]=True

    else:
        print("No eclipse_data_csv passed to does_eclipse_data_exist")
        data_check_dict=None

    return data_check_dict

def acoustic_power(sample_rate, data):
    """
    Calculates the power of the signal.

    Args:
    - Data (np.array): amplitude of signal as given from wavfile.read.
    - sample_rate (float): Data sample rate

    Returns:
    - Time (np.array): Array of seconds from the start of the wave file
    - data np.array): Power of the signal at all frequencies at that time.
    """
    # Handle stereo files (convert to mono if necessary)
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)  # Average channels to get mono

    # Calculate the time axis in seconds
    time = np.linspace(0, len(data) / sample_rate, num=len(data))

    # Calculate the power of the signal (squared amplitude)
    power = data**2

    return time, data

def power_in_frequency_range_welch(sample_rate, data, freq_range, 
                                        segment_duration=1):
                
    """
    Calculates the power of the signal within a specific frequency range
    as determined by Welch's method, as a function of time.

    Args:
    - sample_rate (float): Sample rate of the recording
    - data (np.array): data from the .WAV file
    - freq_range (float list): frequency range in Hz.
    - segment_duration (float): Duration (in seconds) for each segment used by Welch's method.

    Returns:
    - time_bins (np.array)
    - power_bins (np.array)
    """
    # Read the WAV file
    #sample_rate, data = wavfile.read(file_path)

    x1=min(freq_range)
    x2=max(freq_range)

    # Handle stereo files by converting them to mono (averaging channels)
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Define the segment length in samples for Welch's method
    segment_length = int(segment_duration * sample_rate)

    # Initialize time bins and power storage
    time_bins = []
    power_bins = []

    # Split the signal into overlapping segments for Welch's method
    for i in range(0, len(data) - segment_length, segment_length):
        segment = data[i:i + segment_length]

        # Compute the power spectral density (PSD) using Welch's method
        freqs, psd = scipy.signal.welch(segment, fs=sample_rate, nperseg=segment_length)

        # Extract power within the desired frequency range
        freq_mask = (freqs >= x1) & (freqs <= x2)
        power_in_range = np.sum(psd[freq_mask])

        # Store the time (center of the segment) and power value
        segment_time = (i + segment_length / 2) / sample_rate  # Convert sample index to seconds
        time_bins.append(segment_time)
        power_bins.append(power_in_range)

    return time_bins, power_bins

def mk_esid_site_psd_spreadsheet(freqs, tdb_psd_v_freqs, odb_psd_v_freqs,avg_psd_v_freqs, 
                                 std_error,rel_std_error, eclipse_psd_v_freqs, 
                                 eclipse_psd_v_freqs_rel_to_average, 
                                 number_of_stds,max_num_of_stds, 
                                 gt_2_stds, 
                                 outname=False, Dictionary=False
                                 ):
    """
    """
    dict={
        "Frequency [kiloHertz (kH)]":freqs ,
        "Power Spectral Density (PSD) [Amplitude*Amplitude/(kH)] on 10/12/2024":tdb_psd_v_freqs,
        "PSD on 10/13/2024": odb_psd_v_freqs,
        "Average of 10/12/2024 & 10/13/2024 PSD ((B+C)/2)":avg_psd_v_freqs,
        "Standard Error of 10/12/2024 & 10/13/2024 PSD [Amplitude*Amplitude/(kH)]": std_error,
        "Relative Standard Error of 10/12/2024 & 10/13/2024 PSD (E/D)[No units]":rel_std_error,
        "Eclipse Day (10/14/2024) PSD [Amplitude*Amplitude/(kH)]":eclipse_psd_v_freqs,
        "Eclipse Day PSD Relative to Non-Eclipse Day Average (G/D) [No Units]": eclipse_psd_v_freqs_rel_to_average,
        "Number of Standard Deviations the Relative PSD is from the Average of " + \
            "10/12/2024 & 10/13/2024 PSD ((H - D)/F)":number_of_stds,
        "Is Maximum Number of Standard Deviations (+/-)from the Average? (Y/N)":max_num_of_stds,
        "Is Greater than the +/- 2 Standard Deviation Definition of Scientifically Significant? (Y/N)":gt_2_stds
    }

    df=pd.DataFrame(dict)

    if outname:
        df.to_csv(outname, index=False)

    if Dictionary:
        return dict
    else:
        return df

def mk_relative_psd_master_analysis(ESID, 
                                    max_start, 
                                    max_end, 
                                    eclipse_local_type,
                                    rel_psd_max, 
                                    max_freq,
                                    max_rel_error, 
                                    number_of_stds,
                                    significant,
                                    m2,
                                    outname=False, 
                                    Dictionary=False
                                    ):
    
    """
    """
    
    print("Printing shapes")
    print(np.shape(ESID))
    print(np.shape(max_start))
    print(np.shape(max_end))
    print(np.shape(rel_psd_max)) 
    print(np.shape(max_freq))
    print(np.shape(max_rel_error))
    print(np.shape(number_of_stds))
    print(np.shape(significant))
    print("End printing shapes")

    dict={
        "ESID":str(ESID).zfill(3),
        "Start Time (UTC)":max_start,
        "End Time (UTC)":max_end,
        "Eclipse Type":eclipse_local_type,
        "10/14/2023 Maximum Relative PSD (Maximum of Site Spreadsheet Column I) [No Units]":rel_psd_max,
        "Frequency of Maximum Relative PSD Difference on 10/14/2023 [kiloHertz]":max_freq,
        "Relative Error of the Two Days Before at the Frequency of Maximum Relative PSD Difference [No Units]":max_rel_error,
        "Maximum Relative PSD on 10/14/2023 / Relative Error of the Two Days Before [No Units]":number_of_stds,
        "Is this a scientifically defined significant change (Is H > 2 or H < -2?) [Y/N]":significant #, "M2":m2
        }


    df=pd.DataFrame(dict, index=[0])

    if outname:
        if os.path.exists(outname):
            df.to_csv(outname, 
                      mode="a", 
                      index=False, 
                      header=False
                      )
        else:
            df.to_csv(outname, 
                      index=False, 
                      header=True
                      )

    if Dictionary:
        return dict
    else:
        return df
    
def mk_rel_psd_plot(ESID, eclipse_day_string,
                    tdb_freqs_out, tdb_psd,
                    odb_freqs_out, odb_psd, 
                    ecl_freqs, ecl_psd, 
                    freqs_range, 
                    plot_main_title=False,
                    outname=False,
                    verbose=False,
                    Hertz=False):
    """
    """
    ###########################################################################
    #Local variable definitions
    if not plot_main_title:
        plot_main_title="Relative Power Spectral Density at Site #"
        plot_main_title=plot_main_title+str(ESID).zfill(3)+"\n on "
        plot_main_title=plot_main_title+eclipse_day_string+" Eclipse Maximum Time vs.\n"
        plot_main_title=plot_main_title+"Same Time Trame on 2 Non-Eclipse Days"
    
    if not Hertz:
        to_kHz=1000
        x_axis_freq_label="Frequency kiloHertz [Cricket Frequencies (2-8 kHz)]"

    else:
        to_kHz=1
        x_axis_freq_label="Frequency Hertz [Cricket Frequencies (2000-8000 Hz)]"

    label1="Eclipse Day Relative PSD"
    label2="Average of 2 Non-Eclipse Days Relative PSD"
    label3="2 Relative Standard Errors"
    y_axis_label="Relative Power Spectral Density (RPSD)"
    ###########################################################################
    #Calculate and plot the Relative PSD in the frenquency range
    #relative_psd()

    #Calculat the average of the two day before and one day before 
    # recordings and the common interpreted frequencies of the 
    # average.
    interp_freqs, avg_psd, avg_psd_std=compute_average_and_std(
                 tdb_freqs_out, tdb_psd, 
                 odb_freqs_out, odb_psd)
    
    # Interpolate ecl_psd values to the interp_freqs axis
    interp_eclipse_day_psd=np.interp(
        interp_freqs, 
        ecl_freqs, 
        ecl_psd,
        left=ecl_psd[0],
        right=ecl_psd[-1])
    
    # Use np.where to find the indices of elements between the range  (inclusive)
    indices1 = np.where(
        (interp_freqs >= np.min(freqs_range)) 
        & (interp_freqs <= np.max(freqs_range))
        )[0]
    
    freqs_in_range=interp_freqs[indices1]
    avg_psd=avg_psd[indices1]
    avg_psd_std=avg_psd_std[indices1]
    twice_standard_error=2.0 * avg_psd_std    
    relative_error=avg_psd_std/avg_psd
    relative_2_times_error=twice_standard_error/avg_psd
    interp_eclipse_day_psd=interp_eclipse_day_psd[indices1]

    relative_psd=interp_eclipse_day_psd/avg_psd

    one_line=np.ones(len(relative_psd))

    fig=plt.figure()
    plt.title(plot_main_title)

    # Plot the average with standard deviation error bars

    # Overplot twice the standard error
    plt.errorbar(freqs_in_range/to_kHz, one_line, 
                 yerr=relative_2_times_error, 
                 fmt='none',
                 label=label3,
                 capsize=4.5,
                 alpha=0.7, 
                 ecolor='red',
                 )
            
    # Overplot one standard error
    plt.errorbar(freqs_in_range/to_kHz, one_line, 
                 yerr=relative_error, 
                 fmt='none', 
                 ecolor='red', 
                 elinewidth=2, 
                 capsize=4,
                 alpha=0.7
                 )
    
    #Plot a line showing all ones.
    plt.plot(freqs_in_range/to_kHz, 
             one_line, 
             color='blue', 
             linestyle=':', 
             linewidth=2.5, 
             label=label2
             )       
    # Overlay the eclipse day data  with a different style
    plt.plot(freqs_in_range/to_kHz, relative_psd, 
             label=label1, 
             color='orange', 
             linewidth=2.5, 
             linestyle='solid'
             )
            
    # Set the y-axis to semilog scale
    #plt.yscale('log')
    #set the range
    plt.xlim(freqs_range[0]/to_kHz, freqs_range[1]/to_kHz)
           
    ymax=1.3*np.max([np.max(relative_psd), 
                      np.max(np.absolute(1.0+relative_2_times_error))]
                      )
    ymin=np.min([np.min(relative_psd), 
                      np.min(np.absolute(1.0-relative_2_times_error))]
                      )-1.3

    plt.ylim(ymin, ymax)
    plt.xlabel(x_axis_freq_label)
    plt.ylabel(y_axis_label)
    plt.legend(loc='upper center', shadow=True, fontsize='large')
    
    if outname: 
        plt.savefig(outname)
        if verbose: print("Saved file "+outname)
     
    plt.close(fig)
    return plt

def get_audiomoth_temperature(directory,):
    import re
    import csv
    from os import listdir
    from os.path import isfile, join
    from datetime import datetime, timezone, timedelta
    directory = "."
    COMMENT_START = 0x38
    COMMENT_LENGTH = 0x180
    files = [f for f in listdir(directory) if isfile(join(directory, f)) and ".WAV" in f]
    
    with open("comments.csv", "w", newline="") as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=",")
        csvWriter.writerow(["Index", "File", "Time", "Battery (V)", "Temperature (C)", "Comment"])
        
        for i, fi in enumerate(sorted(files)):
            with open(join(directory, fi), "rb") as f:
            # Read the comment out of the input file
                f.seek(COMMENT_START)
                comment = f.read(COMMENT_LENGTH).decode("ascii").rstrip("\0")
                # Read the time and timezone from the header
                ts = re.search(r"(\d\d:\d\d:\d\d \d\d/\d\d/\d\d\d\d)", comment)[1]
                tz = re.search(r"\(UTC([-|+]\d+)?:?(\d\d)?\)", comment)
                hrs = 0 if tz[1] is None else int(tz[1])
                mins = 0 if tz[2] is None else -int(tz[2]) if hrs < 0 else int(tz[2])
                timestamp = datetime.strptime(ts, "%H:%M:%S %d/%m/%Y")
                timestamp = timestamp.replace(tzinfo=timezone(timedelta(hours=hrs, minutes=mins)))
                # Read the battery voltage and temperature from the header
                battery = re.search(r"(\d\.\d)V", comment)[1]
                temperature = re.search(r"(-?\d+\.\d)C", comment)[1]
                # Print the output row
                csvWriter.writerow([i, fi, timestamp.isoformat(), battery, temperature, comment])
