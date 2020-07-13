# import sys

# sys.path.append('/home/lotfi/pfe/PFE')

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE

from .BaseClassifier import Classifier

DrDoSDNSClassifier = Classifier({

	'model_class' : RandomForestClassifier,
	'model_args' : {

		'max_features' : 'auto'
	},
	'scaler_class' : MinMaxScaler,
	'use_scaler' : False,
	'balancer_class' : SMOTE,
	'balancer_args' : {

		'random_state' : 10
	},
	'dataset_path' : '/home/lotfi/pfe/DDOS_datasets/final_datasets/DrDoS_DNS.csv'
})

DrDoSDNSClassifier.load()