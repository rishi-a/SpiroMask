from model import *
from downsample import *
from silence_removal import *

class pipeline:
	def __init__(self,folder,sample_rate=8000,classes = ["breathing","non_breathing"], classifier_type = "logisticregression",classifier_name="LRtemp",feature_list_given=[1,2,4,5,6,7,8,9,10],class_to_extract =0):
		self.folder = folder
		self.sample_rate = sample_rate
		self.classes = classes
		self.classifier_type = classifier_type
		self.classifier_name = classifier_name
		self.feature_list_given = feature_list_given
		self.class_to_extract = class_to_extract
		self.model = speech_removal_model(classes,classifier_type,classifier_name,feature_list_given)


	def extract_breathing_samples(self,desilence_data = False,downsample_data=False):
		if downsample_data:
			downsample_folder(self.folder,self.sample_rate,"./downsampled")
			self.folder = "./downsampled"
			print("downsampled data saved")
		if desilence_data:
			remove_silence_folder(self.folder,output_folder="./desilenced_segments")
			self.folder = "./desilenced_segments"
			print("desilenced data saved")
		self.predict_and_save_folder(self.folder,output_folder="./breathing_segments")
	
	def predict_and_save_folder(self,folder,output_folder):
		types = (folder + os.sep + '*.wav',)

		if os.path.exists(output_folder) and output_folder != ".":
			shutil.rmtree(output_folder)
		os.makedirs(output_folder)

		files_list = []
		for files in types:
			files_list.extend(glob.glob(files))
		for f in files_list:
			file_name = f.split("/")[-1]
			class_ind = aT.file_classification(f, self.classifier_name,self.classifier_type,feature_list_given=self.feature_list_given)[0]
			if class_ind ==self.class_to_extract:
				sr,y =read(f)
				write("{0}/{1}".format(output_folder,file_name),sr,y)
		print("breathing segments saved")

# p = pipeline("data",classifier_name="./trained_model_data/LRtemp")
# p.extract_breathing_samples(desilence_data=True,downsample_data=True)


