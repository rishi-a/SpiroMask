import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
import os
import glob


def resample_flow_volume_file(file,num_samples):
    df = pd.read_csv(file,usecols = [0,1],names=["Volume","Flow"])
    vol = df["Volume"].to_numpy()
    flow = df["Flow"].to_numpy()

    maxx_vol = vol[-1]
    x_to_interp = np.arange(0,maxx_vol,(maxx_vol/num_samples)) 

    y_interp = np.interp(x_to_interp,vol,flow)
    return x_to_interp,y_interp



def create_interpolated_gt_dataset(folder,num_samples,output_folder="./"):
    types = (folder + os.sep + '*.csv',)  # the tuple of file types
    files_list = []

    for files in types:
        files_list.extend(glob.glob(files))
    
    for file in files_list:
        print(file)
        x,y = resample_flow_volume_file(file,num_samples)
        df_tmp = pd.DataFrame({"Volume":x,"Flow":y})
        df_tmp.to_csv(output_folder+"/"+file.split("/")[-1])



def get_windowed_samples(file1,file2,window_size,normalized=True):

    lst1 = pd.read_csv(file1)['Flow'].to_numpy()
    lst2 = pd.read_csv(file2)['Flow'].to_numpy()
    
    if normalized:
	    lst1 = (lst1-min(lst1))/(max(lst1)-min(lst1))
	    lst2 = (lst2-min(lst2))/(max(lst2)-min(lst2))
	    

    min_len = min(len(lst1),len(lst2))
    lst_final1 = []
    lst_final2 = []
    for i in range(min_len-window_size):
        lst_final1.append(lst1[i:i+window_size])
        lst_final2.append(lst2[i:i+window_size])

    lst_final1 = np.array(lst_final1)
    lst_final2 = np.array(lst_final2)
    return lst_final1,lst_final2
    
def create_npy_dataset(X_folder,y_folder,files_list,window_size):
	# files list is file name without file extension
	# files_list = [0,1,3,4,8,9,10]

    output_arr_X = None
    output_arr_y = None
    
    for file in files_list:
        arr_temp1,arr_temp2 = get_windowed_samples("{0}/{1}.csv".format(X_folder,file),"{0}/{1}.csv".format(y_folder,file),window_size)
        if output_arr_X is None:
            output_arr_X = arr_temp1
            output_arr_y = arr_temp2
        else:
            output_arr_X = np.concatenate([output_arr_X,arr_temp1],axis=0)
            output_arr_y = np.concatenate([output_arr_y,arr_temp2],axis=0)
    return output_arr_X,output_arr_y


def predict_entire_curve(model,file,window_size):
        lst1 = pd.read_csv(file)['Flow'].to_numpy()
        lst1 = (lst1-min(lst1))/(max(lst1)-min(lst1))
    
        X = []
        for i in range(len(lst1)-window_size):
            X.append(lst1[i:i+window_size])

        X = np.array(X)
        X = X.reshape(len(X),599,1)
        
        ans = np.array([0.0]*(len(lst1)-window_size))
        y = model.predict(X)

        for i in range(len(y)):
            try:
                ans[i:i+window_size] += y[i]
            except:
                pass
        ans = ans/window_size
        return ans
        