from utils import *


###############################################
'''
function name : extract_tidal_params_file()
input: wav file path
output :(Ti,Te,Rf,VT)

			Ti : inspiration time,
			Te : expiration time
			Rf : no of breaths per minute
			VT : Tidal Volume estimate
'''
def extract_tidal_params_file(file):
	file  = convert_txt_to_audio(file)
	file  = preprocess_file(file)
	return get_parameters(file)
################################################



def extract_tidal_params_folder(folder):

	types = (folder + os.sep + '*.txt',)  # the tuple of file types
	files_list = []
	for files in types:
		files_list.extend(glob.glob(files))

	Ti_lst = []
	Te_lst = []
	Rf_lst = []
	VT_lst = []

	for file in files_list:
		(Ti,Te,Rf,VT) = extract_tidal_params_file(file)
		Ti_lst.append(Ti)
		Te_lst.append(Te)
		Rf_lst.append(Rf)
		VT_lst.append(VT)

	df_tidal_params = pd.DataFrame(
	{'file' : files_list,
		'Ti': Ti_lst,
		'Te': Te_lst,
		'Rf': Rf_lst,
		'VT':VT_lst
	})
	# print(df_tidal_params)
	
	try :
		os.makedirs("extrated_params")
	except:
		pass

	df_tidal_params.to_csv("extrated_params/tidal_params.csv")
	print("params successfully saved")


folder = "raw_data"
extract_tidal_params_folder(folder)