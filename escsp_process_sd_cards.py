#
import escsp 


#Steps in Process
#Define:
#Spreadsheet path
#Path to USB MicroSD reader
data_card_path='/Volumes/Untitled/'
#Path to data storage folder
data_path='/Volumes/'
#Path to folder within data storage folder for correct Level 0 data
#Path to folder within data storage folder for improper timestamp Level 0 data
#Path to folder within data storage folder for data with no config file
#Path to folder for 
#Open spreadsheet with kit numbers, serial numbers, lats and longs
#
#Loop that repeats until user is done entering in data sets.
continue_loop=True
while continue_loop == True:
#Find MemoryCard
#Make list of wave files on data card.
#Read the config.txt file of the data card. 

#If there is no config.txt or data files, alert the user and make kit # folder in a 
#   special folder for corrupt data.
#Get the serial number from the config.txt file
    serial_number=get_am_serial_number_from_config(config_file)

#Caluclate the start time of each file
#Sort list of files by start time
#If start time is less than a certain date, put it into a a special folder
#if start time is within the eclipse protocol, but it in a folder to be analyzed.