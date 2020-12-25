import os
import glob
import ntpath
import shutil
import librosa
from scipy.io.wavfile import read,write
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.io.wavfile import read,write
import argparse
from time import time

def remove_silence_file(file,resolution=100, window_duration=0.1, minimum_power=0.0001,output_folder = "./desilenced_segments"):   

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
        if int(stop[i])-int(start[i]) >= sample_rate/2:
            write("{0}/{1}_segment_{2}.wav".format(output_folder,filename,i),sample_rate,audio[int(start[i]):int(stop[i])])

def remove_silence_folder(folder,output_folder="./desilenced_segments"):
    types = (folder + os.sep + '*.wav',)
    files_list = []
    for files in types:
        files_list.extend(glob.glob(files))

    for f in files_list:
        remove_silence_file(f,output_folder=output_folder)

# remove_silence_folder("data")