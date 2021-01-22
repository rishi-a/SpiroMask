import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
import math
import ruptures as rpt
from scipy import signal
from math import sqrt
from scipy.io import wavfile
from scipy.signal import butter, lfilter, filtfilt
import os
import glob
import ntpath
import shutil
import librosa
from scipy.io.wavfile import read,write
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import argparse
from time import time
from time import sleep

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from scipy.io import wavfile # package to read WAV file
import pandas as pd
import soundfile as sf

SPINE_COLOR = 'gray'

def latexify(fig_width=None, fig_height=None, columns=1):
    """Set up matplotlib's RC params for LaTeX plotting.
    Call this before plotting a figure.

    Parameters
    ----------
    fig_width : float, optional, inches
    fig_height : float,  optional, inches
    columns : {1, 2}
    """

    # code adapted from http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples

    # Width and max height in inches for IEEE journals taken from
    # computer.org/cms/Computer.org/Journal%20templates/transactions_art_guide.pdf

    assert(columns in [1,2])

    if fig_width is None:
        fig_width = 3.39 if columns==1 else 6.9 # width in inches

    if fig_height is None:
        golden_mean = (math.sqrt(5)-1.0)/2.0    # Aesthetic ratio
        fig_height = fig_width*golden_mean # height in inches

    MAX_HEIGHT_INCHES = 8.0
    if fig_height > MAX_HEIGHT_INCHES:
        print("WARNING: fig_height too large:" + fig_height + 
              "so will reduce to" + MAX_HEIGHT_INCHES + "inches.")
        fig_height = MAX_HEIGHT_INCHES

    params = {
              'axes.labelsize': 8, # fontsize for x and y labels (was 10)
              'axes.titlesize': 8,
              'font.size': 8, # was 10
              'legend.fontsize': 8, # was 10
              'xtick.labelsize': 8,
              'ytick.labelsize': 8,
              'figure.figsize': [fig_width,fig_height],
              'font.family': 'serif'
    }

    matplotlib.rcParams.update(params)


def format_axes(ax):

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color(SPINE_COLOR)
        ax.spines[spine].set_linewidth(0.5)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_tick_params(direction='out', color=SPINE_COLOR)

    return ax

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data,axis = 0)
    return y

def get_duration(df_time):
#     return float(df_time.iloc[-1].split(":")[-1])- float(df_time.iloc[0].split(":")[-1])
    ind = None
    count = 0
    for i in range(1,len(df_time)):
        if df_time.iloc[i].split(".")[0]!=df_time.iloc[i-1].split(".")[0]:
            ind = i
            break
    while df_time.iloc[ind].split(".")[0]==df_time.iloc[ind+1].split(".")[0]:
        ind+=1
        count+=1
#     print(count)
    return len(df_time)/count
def calc_non_silence(audio, fs, sil_threshold=0.05, win_size=0.25, ret="sec"):
    """Calculates total non - silence length in this audio file.

    Keywords:
        audio:          location of the audiofile OR a (samplerate, audiodata) tuple
        sil_threshold:  percentage of the maximum window-averaged amplitude
                        below which audio is considered silent
        win_size:       length of window in sec (audio is cut into windows)
        ret:            the return type; can be one of the following:
                        - "sec": return the number of silent seconds
                        - "frac": return the frac of silence (between 0 and 1)
                        - "amp": return a list of amplitude values (one for each window)
                        - "issil": return an np-array of 0s and 1s (1=silent) for each window
                        - "chunk": return a list of (start, end, is_silent) tuples,
                            with start and end in seconds and is_silent is a boolean"""
    
    """ if isinstance(audio, tuple):
        samplerate, data = audio
    else:
        # read the sample rate and data from the wave file
        samplerate, data = wavfile.read(audio)"""
    
    data = audio
    samplerate = fs
    
    win_frames = int(samplerate * win_size) # number of samples in a window
    win_amps = [] # windows in which to measure amplitude

    for win_start in np.arange(0, len(data), win_frames):
        # Find the end of the window
        win_end = min(win_start + win_frames, len(data))
        # Add the mean amplitude for this frame to the list of window amplitudes
        win_amps.append(np.nanmean(np.abs(data[win_start:win_end])))
        
    # Calculate the minimum threshold for a window to be non-silent
    threshold = sil_threshold * max(win_amps)

    # Find the windows that are non-silent
    sils, = np.where(win_amps >= threshold)

    # The silence length is the number of non-silent windows times the window length
    sil = len(sils) * win_size

    if ret == "sec":
        return sil
    elif ret == "frac":
        return len(sils) / len(win_amps)
    elif ret == "amp":
        return win_amps
    elif ret == "issil":
        return (win_amps >= threshold).astype(int)
    elif ret == "chunk":
        chunks = []
        t0, t1 = 0, 0
        is_sil = win_amps[0] >= threshold
        for wi, amp in enumerate(win_amps):
            winsil = amp >= threshold
            if winsil == is_sil:
                t1 = (wi + 1) * win_size
            else:
                chunks.append((t0*win_size, t1*win_size, is_sil))
                t0 = (wi + 1) * win_size
                is_sil = not is_sil
        chunks.append((t0*win_size, len(win_amps)*win_size, is_sil))
        return chunks
    else:
        raise ValueError("Unknown return format: {}".format(ret))



def remove_silence_file(file,resolution=100, window_duration=0.1, minimum_power=0.5,output_folder = "./desilenced_segments"):   

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    sample_rate,audio = read(file)
    duration = len(audio) / sample_rate # in samples/sec
    iterations = int(duration * resolution)
    step = int(sample_rate / resolution)
    window_length = np.floor(sample_rate * window_duration)
    audio_power = np.square(audio) / window_length #Normalized power to window duration

    start = np.array([])
    stop = np.array([])
    is_started = False
    
    for n in range(iterations):
        power = 10 * np.sum(audio_power[n * step : int(n * step + window_length)]) # sensitive
        if not is_started and power > minimum_power:
            start = np.append(start, n * step + window_length / 2)
            is_started = True
        elif is_started and (power <= minimum_power or n == iterations-1):
            stop = np.append(stop, n * step + window_length / 2)
            is_started = False
    
    if start.size == 0:
        start = np.append(start, 0)
        stop = np.append(stop, len(audio))
        
    start = start.astype(int)
    stop = stop.astype(int)
    
    # We don't want to eliminate EVERYTHING that's unnecessary
    # There should be a little boundary...
    # 200 frame buffer before and after
    
    # minus = ?
    if start[0] > 200:
        minus = 200
    else:
        minus = start[0]
        
    # plus = ?
    if (len(audio) - stop[0]) > 200:
        plus = 200
    else:
        plus = len(audio) - stop[0]
    
    start =  (start - minus)
    stop = (stop + plus)
    signal_filtered =  np.array([])
    
    filename = file.split("/")[-1]
    for i in range (len(start)):
        signal_filtered = np.concatenate([signal_filtered,audio[int(start[i]):int(stop[i])]])
        # print(int(stop[i])-int(start[i]))
#         if int(stop[i])-int(start[i]) >= sample_rate/2:
#             write("{0}/{1}_segment_{2}.wav".format(output_folder,filename,i),sample_rate,audio[int(start[i]):int(stop[i])])
    return start,stop

def get_est_tidal_volume(x,fs):
    x = x/np.max(np.abs(x))
    t = np.arange(0,len(x))/fs
    # get analytic signal
    ax = signal.hilbert(x)
    envelope_hat = np.abs(ax)
    nyq_rate = fs / 2.0
    width = 1.0/nyq_rate # 5 Hz filter transition width.
    ripple_db = 10.0 # stop band attenuation
    fL_hz = 10
    N, beta = signal.kaiserord(ripple_db, width)
    taps = signal.firwin(N, fL_hz/nyq_rate, window=('kaiser', beta))
    envelope_hat_filt = signal.filtfilt(taps, 1,envelope_hat)
    
    estdVolume = np.cumsum(envelope_hat_filt)
    estdVolume = estdVolume/np.sum(estdVolume)
    return estdVolume[-1]

def get_parameters(file):
    start,stop = remove_silence_file(file)
    samplerate,audio = read(file)
#     print(start,stop)
    exhalation_tups = []
    exhalation_sigs = []
    
    for i in range(len(start)-1):
        if int(stop[i])-int(start[i]) >= samplerate/2:
            exhalation_tups.append([start[i]/samplerate,stop[i]/samplerate])
            exhalation_sigs.append(audio[start[i]:stop[i]])
    
    inhalation_tups = []
    start = 0
    for i in (exhalation_tups):
        if start==0:
            if i[0]-start>0.8:
                inhalation_tups.append((start,i[0]))
                start = i[1]
        else:
            inhalation_tups.append((start,i[0]))
            start = i[1]
            
    #ridal volume estimates
    tidal_vol_list = []
    for sigs in exhalation_sigs:
        tidal_vol_list.append(get_est_tidal_volume(sigs,samplerate))            
    
    Te = sum([i[1]-i[0] for i in exhalation_tups])/len(exhalation_tups)
    Ti = sum([i[1]-i[0] for i in inhalation_tups])/len(inhalation_tups)
    Rf = 60/(Ti+Te)  ## no. of breaths per minute
    VT = sum(tidal_vol_list)/len(tidal_vol_list)
    return (Ti,Te,Rf,VT)

def preprocess_file(file):
    sig, fs = librosa.load(file, sr=5000) # Downsample 44.1kHz to 8kHz
    y = butter_highpass_filter(sig, 40 ,fs, 4) 
    write(file,fs,y)
    return file

def convert_txt_to_audio(file):
    df = pd.read_csv(file, sep=" ", header=None)
    # print(df.head)
    df.columns = ["t","amp"]
    duration = get_duration(df["t"])
    samplerate = len(df["amp"])/duration
    sig = df["amp"]
    sig = (sig-sig.mean())/sig.std()
    f = "".join(file.split(".")[:-1]+[".wav"])
    write(f,int(samplerate),sig.to_numpy())
    return f