from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten



def seq_to_seq(window_size):

	model = Sequential()
	model.add(Conv1D(filters=30, kernel_size=10, activation='relu', strides=1,input_shape=(window_size,1)))
	model.add(Conv1D(filters=30, kernel_size=8, activation='relu'))
	model.add(Conv1D(filters=40, kernel_size=6, activation='relu'))
	model.add(Conv1D(filters=50, kernel_size=5, activation='relu'))
	model.add(Conv1D(filters=50, kernel_size=5, activation='relu'))
	model.add(Flatten())
	model.add(Dense(1024, activation='relu'))
	model.add(Dense(window_size, activation='relu'))
	model.compile(loss='mean_squared_error', optimizer='adam', metrics=["mse","mae"])
	
	return model


def seq_to_point(window_size):

	model = Sequential()
	model.add(Conv1D(filters=30, kernel_size=10, activation='relu', strides=1,input_shape=(window_size,1)))
	model.add(Conv1D(filters=30, kernel_size=8, activation='relu'))
	model.add(Conv1D(filters=40, kernel_size=6, activation='relu'))
	model.add(Conv1D(filters=50, kernel_size=5, activation='relu'))
	model.add(Conv1D(filters=50, kernel_size=5, activation='relu'))
	model.add(Flatten())
	model.add(Dense(1024, activation='relu'))
	model.add(Dense(1, activation='relu'))
	model.compile(loss='mean_squared_error', optimizer='adam', metrics=["mse","mae"])
	
	return model

class smart_mask_model:

	def __init__(self,model_type="seq_to_seq",window_size =599):
		self.type = model_type
		self.window_size = window_size

	def train(self,X,y,model_name="trained_model"):
		# remember that shape of X and y is (length,window_size,1)
		# e.g. X_train = X_train.reshape(len(X_train),599,1)

		if self.model_type=="seq_to_seq":
			model = seq_to_seq(self.window_size)
			model.fit(X,y)
			model.save("{0}.h5".format(model_name))

