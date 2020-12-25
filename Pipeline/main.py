from model import *
from downsample import *
from silence_removal import *
from extract_breathing_pipeline import *

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn




# model training on input data

classes = ["breathing","non_breathing","ext_audio"]
classifier_type = "logisticregression"
classifier_name = "LRtemp"
feature_list_given = [1,2,3,4,5,6,7,8]
model = speech_removal_model(classes,classifier_type,classifier_name,feature_list_given)
acc = model.train("./training_data")
print("Accuracy ", acc)


''' 
after training, 3 files of prefix <classifier_name> will be generated, 
move them to trained_model_data folder to use for pipeline
'''



'''
pipeline testing : give input folder and trained model with other parameters as input, get extracted breathing segments as output 
no training involved in this step, provide a trained model
'''
# p = pipeline("data",classifier_name="./trained_model_data/LRtemp")
# p.extract_breathing_samples(desilence_data=True,downsample_data=True)

