#import pandas data frame library
import pandas as pd

#import numpy
import numpy as np

#import matplotlib
import matplotlib.pyplot as plt

#import Decision Tree Algorithms
from sklearn.tree import DecisionTreeClassifier

#import K Neirest Neighbors Classifier
from sklearn.neighbors import KNeighborsClassifier

#import Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier

#import split test size
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder, MinMaxScaler

#import metrics module
from sklearn import metrics

#import time to mesure training time
from time import time

#import joblib to persiste and load a classifier
from joblib import dump, load

#import os
from os import path

def factorize_all_data_frame (data_frame) :

	for i in data_frame :

		data_frame[i] = pd.factorize(data_frame[i])[0]

	return data_frame

def clean_dataset (data_frame) :

		assert isinstance(data_frame, pd.DataFrame)

		data_frame.dropna(inplace=True)

		indices_to_keep = ~data_frame.isin([np.nan, np.inf, -np.inf]).any(1)

		data_frame = data_frame[indices_to_keep].astype(np.float64)

		return data_frame

dataset_path = '/home/lotfi/pfe/DDOS_datasets/UDPLag.csv'

#create dataframe
data_frame = pd.read_csv(dataset_path)

print(data_frame.info())

attrs=[
		
	' Protocol',
	' Flow Duration',
	' Total Fwd Packets',
	' Total Backward Packets',
	'Total Length of Fwd Packets',
	' Total Length of Bwd Packets',
	' Fwd Packet Length Mean',
	' Bwd Packet Length Mean',
	'Flow Bytes/s',
	' Flow Packets/s',
	' Fwd Header Length',
	' Bwd Header Length',
	'Fwd Packets/s',
	' Bwd Packets/s',
	' Flow IAT Mean',
	' Label'
]

# select custom attr
data_frame = data_frame[attrs]

UDP_LAG_BENIGNE = data_frame.loc[data_frame[' Label'] == 'BENIGN']

UDP_LAG_BENIGNE= UDP_LAG_BENIGNE.loc[data_frame[' Protocol'] == 17]

udp_benign_line = UDP_LAG_BENIGNE.iloc[1521:1561,:]

UDP_LAG_BENIGNE = UDP_LAG_BENIGNE.iloc[:200]

UDP_LAG_BENIGNE.to_csv('/home/lotfi/pfe/DDOS_datasets/UDPLag/UDPLag_BENIGNE.csv', index=False)

UDP_LAG = data_frame.loc[data_frame[' Label'] == 'UDP-lag']

UDP_LAG= UDP_LAG.loc[data_frame[' Protocol'] == 17]

udp_lag_line = UDP_LAG.iloc[3000:3040,:]

UDP_LAG = UDP_LAG.iloc[:200]

BALANCED_UDP = pd.concat(objs=[UDP_LAG_BENIGNE, UDP_LAG], join='inner')

UDP_LAG.to_csv('/home/lotfi/pfe/DDOS_datasets/UDPLag/UDPLag.csv', index=False)

BALANCED_UDP.to_csv('/home/lotfi/pfe/DDOS_datasets/UDPLag/BALANCED_UDP.csv', index=False)

data_frame = pd.read_csv('/home/lotfi/pfe/DDOS_datasets/UDPLag/BALANCED_UDP.csv')

##shuffle
data_frame = data_frame.reindex(np.random.permutation(data_frame.index))

encoder = LabelEncoder()

data_frame[' Label'] = encoder.fit_transform(data_frame[' Label'])

data_frame = clean_dataset(data_frame)

unseen_mixed_data = pd.concat(objs=[udp_benign_line, udp_lag_line], join='inner')

##shuffle
unseen_mixed_data = unseen_mixed_data.reindex(np.random.permutation(unseen_mixed_data.index))

unseen_mixed_data_labels = encoder.transform(unseen_mixed_data[' Label'])

unseen_mixed_data.drop(columns=[' Label'], inplace=True)

unseen_mixed_data = clean_dataset(unseen_mixed_data)

X = np.array(data_frame.drop(columns=[' Label']))

#create y
y = np.array(data_frame[' Label'])

#split dataset into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#create classifier or model

classifier = DecisionTreeClassifier(criterion="entropy")

#classifier = KNeighborsClassifier()

classifier = RandomForestClassifier(criterion="entropy")

#mesure the trauning time
start = time()

classifier.fit(X_train, y_train)

feat_importances = pd.Series(classifier.feature_importances_, index=unseen_mixed_data.columns).sort_values(ascending=False)

feat_importances.plot(kind="barh")

plt.show()

end = time() - start

print(f'training time is : {end}')

predictions = classifier.predict(unseen_mixed_data)

labels = list(map(int, predictions))

confusion_matrix = metrics.confusion_matrix(unseen_mixed_data_labels, predictions)

classification_report = metrics.classification_report(unseen_mixed_data_labels, predictions, labels=np.unique(y))

print('confusion matrix :')

print(confusion_matrix)

print('classification report :')

print(classification_report)