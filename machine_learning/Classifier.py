import pandas as pd 
import numpy as np 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
#import matplotlib
import matplotlib.pyplot as plt
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

		self.use_scaler = params['use_scaler']

		self.labelEncoder = LabelEncoder()

		self.X = None

		self.y = None


	####
	# check if the given model exists 
	# @return {Boolean}
	####
	def is_exists (self) : 

		return path.exists(f'{self.modelClass.__name__}.joblib') and path.exists(f'{self.scalerClass.__name__}.joblib')

	"""
		clean the dataset from nan and inf
	"""
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

		self.data_frame = pd.read_csv(self.dataset_path)

		self.data_frame['label'] = self.labelEncoder.fit_transform(self.data_frame['label'])

		self.X = self.data_frame.drop(columns=['label'])

		if self.use_scaler == True :

			self.scaler = self.scalerClass()

			self.X = self.scaler.fit_transform(self.X)

		self.y = self.data_frame['label']

		if self.is_exists() :

			self.classifier = joblib.load(f'{self.modelClass.__name__}.joblib')

			self.scaler = joblib.load(f'{self.scalerClass.__name__}.joblib')

			self.data_frame = pd.read_csv(self.dataset_path)

		else :

			print('classifier not exists', self.classifier, self.scaler)

			self.build()

	####
	## Build and train the model
	## 
	###
	def build (self) :

		if self.classifier == None :

			print('build')

			#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

			self.classifier = self.modelClass()

			self.classifier.fit(self.X, self.y)

			print('classifier training finished')

			self.persiste_classifier()

			self.persiste_scaler()

	def predict_flows (self, flows) :

		# feat_importances = pd.Series(self.classifier.feature_importances_, index=self.X.columns).sort_values(ascending=False)

		# feat_importances.plot(kind="barh")

		# plt.show()

		print(flows)

		predictions = self.classifier.predict(flows)

		labels = list(map(int, predictions))

		labels = self.labelEncoder.inverse_transform(labels)

		print('prediction', labels)


