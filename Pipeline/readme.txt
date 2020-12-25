
# how to work with the pipeline

run following commands:


Important step : only install pyaudioanalysis using following command (several changes have been made in the library)
	pip install -e ./pyAudioAnalysis

pip install -r requirements.txt
pip install -r ./pyAudioAnalysis/requirements.txt

Now required packages have been installed

# To train a new model use training() function in Class speech_removal_model, other details are provided in model.py

# To directly extract breathing sounds from a folder, edit last two lines of extract_breathing_pipeline.py to provide required parameters, run the file. Breathing samples will be collected in output folder named "breathing_segments"