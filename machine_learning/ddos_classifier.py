import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from datetime import datetime, date
import joblib
from os import path

class Classifier () :

	def __init__ (self, params) :

		self.modelClass = params['model_class']

		self.dataset_path = params['dataset_path']

		self.data_frame = pd.DataFrame()

		self.classifier = None

		self.scaler = MinMaxScaler()

		self.labelEncoder = LabelEncoder()


	####
	# check if the given model exists 
	# @return {Boolean}
	####
	def is_exists (self) : 

		return path.exists(f'{self.classifier.__class__.__name__}.joblib')

	####
	# Clean the data frame
	# @return {Void}
	###
	def clean_dataset (self) :

		assert isinstance(self.data_frame, pd.DataFrame)

		self.data_frame.dropna(inplace=True)

		indices_to_keep = ~self.data_frame.isin([np.nan, np.inf, -np.inf]).any(1)

		self.data_frame = self.data_frame[indices_to_keep].astype(np.float64)

	####
	## Persiste the given classfier
	## @return {Void}
	###
	def persiste_classifier (self) :

		joblib.dump(self.classifier, f'{self.classifier.__class__.__name__}.joblib')

	####
	## Persiste the given scaler
	## @return {Void}
	###
	def persiste_scaler (self) :

		joblib.dump(self.scaler, f'{self.scaler.__class__.__name__}.joblib')

	####
	## Build and train the model
	## 
	###
	def build (self) :

		self.data_frame = pd.read_csv(self.dataset_path)

		self.data_frame.rename(columns={' Label' : 'label'}, inplace=True)

		self.data_frame['label'] = self.labelEncoder.fit_transform(self.data_frame['label'])

		self.clean_dataset()

		X = self.data_frame.drop('label', axis=1)

		X = self.scaler.fit_transform(X)

		y = self.data_frame['label']

		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

		self.classifier = self.modelClass()

		start = datetime.now().replace(microsecond=0)

		classifier.fit(X_train, y_train)

		end = datetime.now().replace(microsecond=0)

		duration = end - start

		persiste_classifier()

		persiste_scaler()
		   
		prediction = classifier.predict(X_test)

		print('timing : {} '.format(duration))

		print(classification_report(y_test, prediction))

classifier = Classifier({

	'model_class' : RandomForestClassifier,
	'dataset_path' : ''
})

classifier.build()


