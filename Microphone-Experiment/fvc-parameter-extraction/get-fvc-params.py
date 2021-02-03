import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
#from scipy.io import wavfile # package to read WAV file
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

import sys

if sys.argv[1] == 'c':
	mypath="clothData/"
else:
	mypath="n95Data/"


#script for reading files from json folder

#mypath="jsonDataRohit/"
(_, _, filenames) = next(os.walk(mypath))

rPEF = []
rFEV1 = []
rFVC = []
fileList = []

for file in filenames:
    print("Reading:", file)
    fileList.append(file)
    fig = plt.subplots(figsize=(10,8))
    x = pd.read_json(mypath+file, orient='keys')['payload']['values']
    
    plt.subplot(2, 2, 1)
    plt.plot(x)
    plt.ylabel('Amplitude')
    plt.xlabel('Samples')
    
    #sampling rate is 16Khz
    fs = 16000
    x = x/np.max(np.abs(x))
    #detect the starting point of FVC
    fvcStartIndex = np.where(x>=0.50)
    #move back 1 second from the point FVC started and go till 4 seconds
    x = x[fvcStartIndex[0][0]-5000:fvcStartIndex[0][0]-5000+56000]
    t = np.arange(0,len(x))/fs
    
    plt.subplot(2, 2, 2)
    plt.plot(t,x)
    plt.ylabel('Amplitude/Estd Flow')
    plt.xlabel('Time')
    

    # get analytic signal
    ax = signal.hilbert(x)
    envelope_hat = np.abs(ax)
    #filter the Hilbert envelope
    nyq_rate = fs / 1.0
    width = 1.0/nyq_rate # 5 Hz filter transition width.
    ripple_db = 10.0 # stop band attenuation
    fL_hz = 10
    N, beta = signal.kaiserord(ripple_db, width)
    taps = signal.firwin(N, fL_hz/nyq_rate, window=('kaiser', beta))
    envelope_hat_filt = signal.filtfilt(taps, 1,envelope_hat)

    envelope_hat_filt_normalized = envelope_hat_filt/np.sum(envelope_hat_filt)
    
    #Corresponds to PEF
    rPEF.append(100000*envelope_hat_filt_normalized.max())
    print("Raw PEF = ",100000*envelope_hat_filt_normalized.max())
    
    #take cumsum of flow and then normalize
    estdVolume = np.cumsum(envelope_hat_filt)
    estdVolume = estdVolume/np.sum(estdVolume)
    
    #FEV1 Estimate
    rFEV1.append(100000*estdVolume[np.where(t==1)[0][0]])
    print("Raw FEV1 = ",100000*estdVolume[np.where(t==1)[0][0]])
    
    plt.subplot(2, 2, 3)
    plt.plot(t,estdVolume,color='red',label='Estimated Volume')
    plt.ylabel('Estimated Volume')
    plt.xlabel('Time')
    
    #FVC Estimate
    rFVC.append(100000*estdVolume[-1])
    print("Raw FVC = ",100000*estdVolume[-1])
    print("\n\n")
    
    plt.subplot(2, 2, 4)
    plt.plot(estdVolume, envelope_hat_filt)
    plt.xlabel('Estimated Volume')
    plt.ylabel('Estimated Flow')
    
    if sys.argv[1] == 'c':
        plt.savefig('clothplots/'+file+'plots.png', bbox_inches='tight')
    else:
        plt.savefig('n95plots/'+file+'plots.png', bbox_inches='tight')

#save the data
rPFT = pd.DataFrame(
    {'Filename': fileList,
     'rPEF': rPEF,
     'rFEV1': rFEV1,
     'rFVC': rFVC
    })

#print("Done Reading files in", mypath[:len(mypath)-1])
rPFT.to_csv(mypath[:len(mypath)-1]+'-rPFT.csv')