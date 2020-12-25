from pyAudioAnalysis import audioTrainTest as aT
import os
import glob
import ntpath
import shutil
import librosa
import soundfile as sf
from pyAudioAnalysis import audioSegmentation as aS
from scipy.io.wavfile import read,write
from pyAudioAnalysis import audioBasicIO as io
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pyAudioAnalysis import audioBasicIO as io
from scipy.io.wavfile import read,write
import argparse
from time import time

# --------------------------------------------------------
# This file contains class speech_removal_model

# functions :
#
# __init__() : 
# 		arguments: 
# 			1) classes : type -> list  ::-> takes a list of classes for classifier e.g ["breathing","non_breathing"]
# 			2) classifier_type : str ::-> e.g "logisticregression"
# 			3) classifier_name : str ::-> name of classifier model to save as e.g "LRtemp"
# 			4) feature_list_given : list ::-> list of features. [numbers from 1 to 10] e.g [1,2]
#
#
# 																																																																																	comments by Rohit
# --------------------------------------------------------


'''
----raw audio data in following format:
folder structure

---- data 
---------training_folder
----------------------class_1 (breathing)
----------------------class_2 (speaking)
----------------------class_3 (ext_sound)
---------testing_folder
----------------------class_1 (breathing)
----------------------class_2 (speaking)
----------------------class_3 (ext_sound)
'''

class speech_removal_model:

	def __init__(self,classes,classifier_type,classifier_name,feature_list_given):
		self.classes = classes
		self.classifier_type = classifier_type
		self.classifier_name = classifier_name
		self.feature_list_given = feature_list_given

	def train(self,training_folder):
		training_folder_lst = [training_folder+"/"+i for i in self.classes]
		acc = aT.extract_features_and_train(training_folder_lst, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, self.classifier_type, self.classifier_name, False,feature_list_given=self.feature_list_given)
		# aT.extract_features_and_train(training_folder_lst, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "logisticregression", "LRtemp", False,feature_list_given=feature_list_given)
		return acc

	def evaluate_model_folder(self,testing_folder,class_under_consideration):
		testing_folder_lst = [testing_folder+"/"+i for i in self.classes]
		# cm, thr_prre, pre, rec, thr_roc, fpr, tpr = aT.evaluate_model_for_folders(["downsampled/testing_data/breathing/", "downsampled/testing_data/non_breathing/"], "LRtemp", "logisticregression", "breathing",feature_list_given=feature_list_given)
		cm, thr_prre, pre, rec, thr_roc, fpr, tpr = aT.evaluate_model_for_folders(testing_folder_lst, self.classifier_name, self.classifier_type, class_under_consideration,plot=False,feature_list_given=self.feature_list_given)
		numerator = sum([cm[i][i] for i in range(len(cm))])
		denominator = np.sum(cm)
		acc = numerator/denominator
		return acc
	
	def find_prediction_time_folder(self,folder):
		#put a bunch of files in this folder

		types = (folder + os.sep + '*.wav',)
		files_list = []
		for files in types:
			files_list.extend(glob.glob(files))
		start = time.time()
		for f in files_list:
			aT.file_classification(f, self.classifier_name,self.classifier_type,feature_list_given=self.feature_list_given)
		end = time.time()
		return(end-start,len(files_list))

	def predict_file(file):
		return aT.file_classification(file, self.classifier_name,self.classifier_type,feature_list_given=self.feature_list_given)
	