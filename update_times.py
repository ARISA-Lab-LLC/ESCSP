#update_times.py

from escsp import *

folder = "/media/tracy/ESCSPA00/Total_Time_Adjusted_Data/ESID#232/"
start_time="2024-04-05 15:20:00"
timezone_str='US/Central'
time_format="%Y-%m-%d %H:%M:%S"
move=False

files=glob.glob(os.path.join(folder,"*.WAV"))
verbose=1
adjust_am_datetime(files, start_time, timezone_str, time_format_in=time_format, move=move, verbose=verbose)

