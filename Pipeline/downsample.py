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
import os

def downsample_folder(folder,sample_rate=8000,output_folder = "./downsampled"):

    types = (folder + os.sep + '*.wav',)  # the tuple of file types

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    files_list = []
    for files in types:
        files_list.extend(glob.glob(files))

    if os.path.exists(output_folder) and output_folder != ".":
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    for f in files_list:
        filename = f.split("/")[-1]
        y,sr = librosa.load(f, sr=sample_rate)
        write(output_folder+"/"+filename,sr,y)

# downsample_folder("desilenced_segments")