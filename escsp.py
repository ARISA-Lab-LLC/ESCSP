#escsp_audio_change.py
###########################################################################
#Import Libraries section
import pickletools
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
from scipy.misc import derivative
import copy
###########################################################################

def get_audio_start_time(type="NPS"):
    """ Return the start time of a wave file based on the filename  """
