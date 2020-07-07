from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler

from machine_learning.Classifier import Classifier

ddos_classifier = Classifier({

	'model_class' : DecisionTreeClassifier,
	'model_args' : {},
	'scaler_class' : MinMaxScaler,
	'use_scaler' : False,
	'dataset_path' : '/home/lotfi/pfe/DDOS_datasets/final_datasets/UDPLag.csv'
})

ddos_classifier.load()