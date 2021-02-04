import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read,write
import serial



ser = serial.Serial('COM9')

lst = []

print("press Enter to start recording")
input()
print("Recording data .... Press Ctrl-C to stop recording")


start = time.time()

def a():	
	try:
		var = ser.readline()
		lst.append(var)
	except:
		end = time.time()
		


while True:
	try:
		a()
	except:
		break

print(lst)
lst = pd.Series(lst)



print("write y to accept")
print("write n to reject")
inp = input()

if inp == "y":
	print("write filename")
	f = input()
	# write("recorded_data/"+f+".wav",int(samplerate),lst.to_numpy())
	lst.to_csv(f)
else:
	print("bye")

