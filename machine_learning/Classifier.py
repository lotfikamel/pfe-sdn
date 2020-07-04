import pandas as pd 
import numpy as np 
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

		self.scalerClass = params['scaler_class']

		self.scaler = None

		self.labelEncoder = LabelEncoder()

		self.rename_columns = {

			' Label' : 'label'
		}


	####
	# check if the given model exists 
	# @return {Boolean}
	####
	def is_exists (self) : 

		return path.exists(f'{self.modelClass.__name__}.joblib') and path.exists(f'{self.scalerClass.__name__}.joblib')

	def clean_dataset (self) :

		self.data_frame.replace([np.inf, -np.inf], np.nan).dropna(inplace=True)

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
	# load classifier if persisted else build new one
	# @return {Object}
	###
	def load (self) : 

		if self.is_exists() :

			self.classifier = joblib.load(f'{self.modelClass.__name__}.joblib')

			self.scaler = joblib.load(f'{self.scalerClass.__name__}.joblib')

			self.data_frame = pd.read_csv(self.dataset_path)

			self.data_frame.rename(columns=self.rename_columns, inplace=True)

		self.build()

	####
	## Build and train the model
	## 
	###
	def build (self) :

		if self.classifier == None and self.scaler == None : 

			self.data_frame = pd.read_csv(self.dataset_path)

			self.data_frame.rename(columns=self.rename_columns, inplace=True)

			self.data_frame['label'] = self.labelEncoder.fit_transform(self.data_frame['label'])

			self.clean_dataset()

			X = np.array(self.data_frame.drop('label', axis=1))

			self.scaler = self.scalerClass()

			X = self.scaler.fit_transform(X)

			y = np.array(self.data_frame['label'])

			X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

			self.classifier = self.modelClass()

			start = datetime.now().replace(microsecond=0)

			self.classifier.fit(X_train, y_train)

			end = datetime.now().replace(microsecond=0)

			duration = end - start

			self.persiste_classifier()

			self.persiste_scaler()
			   
			prediction = self.classifier.predict(X_test)

			print('timing : {} '.format(duration))

			print(classification_report(y_test, prediction))


