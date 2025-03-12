#update_times.py

from escsp import *

top_in_folder = "/media/tracy/2024_Total_Data_Pease/2024_Total_Eclipse_Data_Rd_2/"
top_out_folder = "/media/tracy/2024_Total_Data_Pease/2024_Total_Eclipse_Data_Rd_2/"
input_csv="Manual_times_Pease_Rd2c.csv"
time_format="%Y-%m-%d %H:%M:%S"
verbose=1
test=False

df=pd.read_csv(input_csv, 
               dtype = {'ESID': str,  
                        'Start Date': str, 
                        'Start Time': str, 
                        'Time Zone': str,
                        'Can Update': str,
                        'Not Enough Data':str
                        })

sites_to_update=df["ESID"].values

print(str(len(sites_to_update)))
print(sites_to_update)

#sites_to_update=sites_to_update[0]
for site in sites_to_update:
    can_update=int(df.loc[df['ESID'] == site, 'Can Update'].values[0])

    if can_update >= 1:
     # Find the "Time Zone" value where "ESID" is equal to "site"
        time_zone_value = df.loc[df['ESID'] == site, 'Time Zone'].values[0]
        start_time      = df.loc[df['ESID'] == site, 'Start Date'].values[0]
        start_time      =  start_time + " "+df.loc[df['ESID'] == site, 'Start Time'].values[0]
        start_time=start_time.strip()
        time_zone_value=time_zone_value.strip()

        if verbose:
            print("time_zone_value: "+time_zone_value)
            print("start_time: "+start_time)
    
        if not "ND" in start_time:
            folder=os.path.join(top_in_folder, "ESID#"+str(site).zfill(3))
            files=glob.glob(os.path.join(folder,"*.WAV"))
            updated_folder=os.path.join(top_out_folder, 
                                        "ESID#"+str(site).zfill(3)+
                                        "_2024TotalEclipse_ManualTimeSet")

            if verbose:
                print("In Folder: "+ folder)
                print("updated_folder: "+ updated_folder)
                print("time_zone_value: "+ str(time_zone_value))
                print("start_time: "+ str(start_time))

            if  not test:
                os.system("mkdir "+updated_folder)
            
                adjust_am_datetime(files, start_time, time_zone_value,
                                   time_str=time_format, 
                                   updated_folder=updated_folder, 
                                   verbose=verbose)
            else:
                adjust_am_datetime(files, start_time, time_zone_value, 
                                   time_str=time_format, 
                                   updated_folder=False, 
                                   verbose=verbose)
            
            
    

