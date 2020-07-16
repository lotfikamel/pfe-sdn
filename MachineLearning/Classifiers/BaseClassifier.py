import pandas as pd

import numpy as np

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import confusion_matrix, classification_report

from sklearn.preprocessing import LabelEncoder, MinMaxScaler

from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt

from datetime import datetime, date

import joblib

from os import path

class Classifier () :

	def __init__ (self, params) :

		self.modelClass = params['model_class']

		self.modelArgs = params['model_args']

		self.dataset_path = params['dataset_path']

		self.data_frame = pd.DataFrame()

		self.classifier = None

		self.scalerClass = params['scaler_class']

		self.scaler = None

		self.use_scaler = params['use_scaler']

		self.use_balancer = params['use_balancer']

		self.balancerClass = params['balancer_class']

		self.balancer = None

		self.balancerArgs = params['balancer_args']

		self.labelEncoder = LabelEncoder()

		self.X = None

		self.y = None


	####
	# check if the given model exists 
	# @return {Boolean}
	####
	def is_exists (self) : 

		return path.exists(f'{self.modelClass.__name__}.joblib')

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

		joblib.dump(self.classifier, f'./{self.classifier.__class__.__name__}.joblib')

	####
	## Persiste the given scaler
	## @return {Void}
	###
	def persiste_scaler (self) :

		if self.use_scaler == True :

			joblib.dump(self.scaler, f'./{self.scaler.__class__.__name__}.joblib')

	####
	# load classifier if persisted else build new one
	# @return {Object}
	###
	def load (self) :

		print('load')

		self.data_frame = pd.read_csv(self.dataset_path)

		self.data_frame['label'] = self.labelEncoder.fit_transform(self.data_frame['label'])

		self.X = self.data_frame.drop(columns=['label'])

		self.y = self.data_frame['label']

		if self.use_scaler == True :

			self.scaler = self.scalerClass()

			self.X = self.scaler.fit_transform(self.X)

		if self.use_balancer == True :

			print(self.X.shape)

			self.balancer = self.balancerClass(**self.balancerArgs)

			self.X, self.y = self.balancer.fit_sample(self.X, self.y)

			print(self.X.shape)

		if self.is_exists() :

			print('classifier exists', self.classifier)

			self.classifier = joblib.load(f'./{self.modelClass.__name__}.joblib')

			if self.use_scaler == True :

				self.scaler = joblib.load(f'./{self.scalerClass.__name__}.joblib')

		else :

			print('classifier not exists')

			self.build()

	####
	## Build and train the model
	## 
	###
	def build (self) :

		if self.classifier == None :

			print('build')

			#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

			self.classifier = self.modelClass(**self.modelArgs)

			self.classifier.fit(self.X, self.y)

			print('classifier training finished')

			self.persiste_classifier()

			self.persiste_scaler()

	def predict (self, data) :

		feat_importances = pd.Series(self.classifier.feature_importances_, index=self.X.columns).sort_values(ascending=False)

		print(feat_importances)

		# feat_importances.plot(kind="barh")

		# plt.show()

		predictions = self.classifier.predict(data)

		labels = list(map(int, predictions))

		labels = self.labelEncoder.inverse_transform(labels)

		return labels


