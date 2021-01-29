import serial
import time

import zmq
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read,write



ser = serial.Serial('/dev/ttyACM0')

lst = []

print("press Enter to start recording")
input()
print("Recording data .... Press Ctrl-C to stop recording")


start = time.time()

while True:
	try:
		var = ser.readline()
		lst.append(var)
	except:
		end = time.time()
		break

lst = [int(var.decode("utf-8").replace("\\r\\n","")) for var in lst]

duration = round(end-start,4)
samplerate = int(len(lst)/duration)
t = np.arange(0,duration,1/samplerate)
min_len = min(len(t),len(lst))
t = t[2*samplerate:min_len]
lst = lst[2*samplerate:min_len]


lst = pd.Series(lst)

lst = (lst-lst.mean())/lst.std()

plt.plot(t,lst)
plt.show()

print("write y to accept")
print("write n to reject")
inp = input()

if inp == "y":
	print("write filename")
	f = input()
	write("recorded_data/"+f+".wav",int(samplerate),lst.to_numpy())
else:
	print("bye")