from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler

from Classifier import Classifier

ddos_classifier = Classifier({

	'model_class' : RandomForestClassifier,
	'scaler_class' : MinMaxScaler,
	'dataset_path' : '/home/lotfi/pfe/ddos_dataset.csv'
})

ddos_classifier.load()

print(ddos_classifier.classifier)