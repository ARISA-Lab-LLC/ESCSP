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
#
import scipy
import pandas as pd
from natsort import natsorted
import glob
import numpy as np 
# for visualizing the data 
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
import subprocess
#import moviepy
from tracemalloc import stop
from scipy.misc import derivative
import copy
from moviepy.editor import *
###########################################################################
#
user_images=None
youtube_assets_folder="./YouTube_Assets/"
privacyStatus="private"
#privacyStatus="public"
###########################################################################

def get_audio_start_info(files, type="AudioMoth", verbose=None):
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
        
        if type == "AudioMoth":
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

def read_config():
    """ """
    
    return 

def get_am_serial_number_from_config(FILE):

    return serial_number

def read_escsp_setup():
    """read the escsp_setup.cdat csv file that sets filepaths"""

    return escsp_info

def escsp_read_eclipse_csv(eclipse_data_csv, verbose=None):
    """"""
    if os.path.isfile(eclipse_data_csv) :
        df=pd.read_csv(eclipse_data_csv, header=[0])
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

    else: print('Error! No file named '+eclipse_data_csv)

    return eclipse_info

def escsp_get_eclipse_time_trio(eclipse_info, verbose=None):
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
        max_eclipse= eclipse_info["FirstContactDate"] + " " +eclipse_info["MaxEclipseTimeUTC"] 
        eclipse_start_time=max_eclipse-datetime.timedelta(minutes=3)
        eclipse_end_time=max_eclipse+datetime.timedelta(minutes=3)

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
    
def filename_2_datetime(files, type="AudioMoth", verbose=None):
    """ Return a list if datetimes that correspond to the  """
    if verbose != None: print("Here 1")
    date_times=None
    if len(files) >=1:
        date_times=[]
        for file in [files]:
            #Get the filename
            if verbose != None: print('file= '+file)
            filename=(os.path.basename(file).split(".")[0])
            if verbose != None: print('filename= '+filename)

            if type == "NPS": date_times=None

            if type == "AudioMoth":
                date_string, time_string=filename.split("_")
                if verbose != None: print('date_string= '+date_string)
                if verbose != None: print('time_string= '+time_string)

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

                
                    
        return date_times


def get_files_between_times(files, start_time, end_time):
    """Return only the filepaths for the recording files that are between the start_time & the end_time"""

    #I know there is a better way (more matrix) to do this, but I don't have the time to figure it out.
    return_files=None
    for file in files:
        date_and_time=filename_2_datetime(file, type="AudioMoth")
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

def adjust_am_datetime(files, start_time, move=False, verbose=False):
    """Program to adjust the time of AudioMoth files if the time was not properly set. 
      Requires a set of recording files and a datetime object of the reported start time."""
    files=natsorted(files)
    N_files=len(files)
    updated_file_names = None
    date_and_times=[]
    delta_times=[]
    counter=1
    if len(files) >= 1:
    
        for file in files:  
            if verbose: print("File= "+ file)
            d_and_t_0=filename_2_datetime(file, type="AudioMoth")
            if counter<= N_files-1:
                if verbose: print("Calculating "+files[counter]+" - "+file)
                delta=filename_2_datetime(files[counter], type="AudioMoth")[0]-d_and_t_0[0]
                delta_times.append(delta)

            date_and_times.append(d_and_t_0[0])
            if verbose: print("length of date_and_times= "+str(len(date_and_times)))
            counter+=1
            #if verbose: print(date_and_times)
            
           
    #print(delta_times)

    return delta_times #updated_file_names
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
                    
def filename_2_ESID(file):
    esid=None
    if os.path.isfile(file):
        f=os.path.basename(file)
        #ESID=folder.split("#")[1][0:3]
        esid=f[5:8]

    if os.path.isdir(file):
        f=file.split("/")
        for segment in f:
            if segment[0:4] == 'ESID':
                esid=segment[5:8]
        #f=f[len(f)-2]
        

    if not  os.path.isdir(file) and not os.path.isfile(file):
        print('error in filename_2_ESID')
        print('error in: '+file)
       


    return esid

def escsp_get_psd(folder, plots_folder, filelist=None, verbose=False):
    if verbose: print(folder)
    ESID=filename_2_ESID(folder)
    if verbose: print(ESID)
    plot_1_name=os.path.join(folder, "PSD_plot_"+ESID+".png")
    plot_1a_name=os.path.join(plots_folder, "PSD_plot_"+ESID+".png")
    eclipse_data_csv=os.path.join(folder, "eclipse_data.csv")

    if os.path.isfile(eclipse_data_csv) :
        df=pd.read_csv(eclipse_data_csv, header=[0])
        time_format="%Y-%m-%d %H:%M:%S"
        if verbose: print("success! " + eclipse_data_csv) 
        if eclipse_type == "Annular" or eclipse_type == "Total":
#set the eclipse start time
            second_contact=str(df.iloc[5, 1])+ " " + str(df.iloc[7, 1])
            print(second_contact)
        #eclipse_start_time = datetime.datetime(2023, 10, 14, 17, 34) 
            eclipse_start_time = datetime.datetime.strptime(second_contact, time_format) 
#set the eclipse end time
        #eclipse_end_time = datetime.datetime(2023, 10, 14, 17, 39)
            third_contact = str(df.iloc[5, 1])+ " " + str(df.iloc[8, 1])
            eclipse_end_time =  datetime.datetime.strptime(third_contact, time_format) 
        else:
            max_eclipse=datetime.datetime.strptime(
                str(df.iloc[5, 1])+ " " + str(df.iloc[10, 1]), time_format) 
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


#IF the filelist parameter is set, then write the names of the files to the filelst file.  
        if filelist:
            if os.path.isfile(filelist):
                list_file=filelist
            else:
                list_file=os.path.join(folder, ESID+'_Analysis_Files.csv')
            
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

        if eclipse_files: 
            eclipse_wav, fs_ecl=combine_wave_files(eclipse_files, verbose=verbose)
            #f0, eclipse_psd=scipy.signal.periodogram(eclipse_wav, fs_ecl)
            fig, ax =plt.subplots()
            ax.psd(eclipse_wav, Fs=fs_ecl, color="orange", label="Eclipse Day")

        if two_days_before_files :
            print("Length of filelist: " + str(len(two_days_before_files)))
            two_days_before_wav, fs_tdb = combine_wave_files(two_days_before_files, verbose=verbose)
            #f2, two_days_before_psd=scipy.signal.periodogram(two_days_before_wav, fs_tdb)
            ax.psd(two_days_before_wav, Fs=fs_tdb, color="green", label="Two Days Before")

        if one_day_before_files: 
            one_day_before_wav, fs_odb = combine_wave_files(one_day_before_files, verbose=verbose)
            #f1, one_day_before_psd=scipy.signal.periodogram(one_day_before_wav, fs_odb)
            ax.psd(one_day_before_wav, Fs=fs_odb, color="blue", label="One Day Before")


            legend = ax.legend(loc='upper center', shadow=True, fontsize='large')
            plt.savefig(plot_1_name)
            if verbose: print("Saved file "+plot_1_name)    
            plt.savefig(plot_1a_name)
            if verbose: print("Saved file "+plot_1a_name)
            plt.close(fig)

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
        eclipse_images=[os.path.join(youtube_assets_folder,"Annular_Eclipse_YouTube_Image.png"),
                            os.path.join(youtube_assets_folder,"Partial_Eclipse_YouTube_Image.png"),
                            os.path.join(youtube_assets_folder,"Non-eclipse_days_YouTube_Image_Outdoor_Tree_Picture.png"),
                            os.path.join(youtube_assets_folder,"Total_Eclipse_image_YouTube..png")]
            
        if eclipse_type != None:
            if eclipse_type == "Annular" : 
                eclipse_image_file=eclipse_images[0]
                Photo_Credit="Shutterstock: Stock Photo ID: 1598297254, Contributor Hyserb"
                Photo_Description="Annular Solar Eclipse of the Sun in Hofuf, Saudi Arabia.  "
                Photo_Description=Photo_Description+"Annular solar eclipse over a hazy desert landscape, "
                Photo_Description=Photo_Description+"with a bright ring of the sun visible around the moon. "
                Photo_Description=Photo_Description+"The sky glows in a deep orange hue, enhancing the mystical appearance of the scene."
"
            if eclipse_type == "Partial" : 
                eclipse_image_file=eclipse_images[1]
                Photo_Credit="Credit: Evan Zucker"
                Photo_Description="Silhouette of wind turbines on the horizon during a sunset, "
                Photo_Description=Photo_Description+"with a dramatic crescent solar eclipse visible in the background, "
                Photo_Description=Photo_Description+"casting a warm orange glow in the sky."
"

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
        eclipse_data_csv=os.path.join(folder, "eclipse_data.csv")
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


        
    
    
    
