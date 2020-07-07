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

dataset_path = '/home/lotfi/pfe/DDOS_datasets/final_datasets/TCPSyn.csv'

#create dataframe
data_frame = pd.read_csv(dataset_path)

TCP_BENIGN = data_frame.loc[data_frame['label'] == 'BENIGN']

tcp_benign_line = TCP_BENIGN.iloc[150:187,:]

TCP_BENIGN = TCP_BENIGN.iloc[:149]

TCP_BENIGN.to_csv('/home/lotfi/pfe/DDOS_datasets/TCPSyn/TCPSyn_BENIGNE.csv', index=False)

TCP_SYN = data_frame.loc[data_frame['label'] == 'Syn']

tcp_syn_line = TCP_SYN.iloc[150:187,:]

TCP_SYN = TCP_SYN.iloc[:149]

TCP_SYN.to_csv('/home/lotfi/pfe/DDOS_datasets/TCPSyn/TCPSyn.csv', index=False)

BALANCED_TCP = pd.concat(objs=[TCP_BENIGN, TCP_SYN], join='inner')

BALANCED_TCP.to_csv('/home/lotfi/pfe/DDOS_datasets/TCPSyn/BALANCED_TCP.csv', index=False)

data_frame = pd.read_csv('/home/lotfi/pfe/DDOS_datasets/TCPSyn/BALANCED_TCP.csv')

##shuffle
data_frame = data_frame.reindex(np.random.permutation(data_frame.index))

encoder = LabelEncoder()

data_frame['label'] = encoder.fit_transform(data_frame['label'])

unseen_mixed_data = pd.concat(objs=[tcp_benign_line, tcp_syn_line], join='inner')

##shuffle
unseen_mixed_data = unseen_mixed_data.reindex(np.random.permutation(unseen_mixed_data.index))

print('unseen_mixed_data', unseen_mixed_data['label'].value_counts())

unseen_mixed_data['label'] = encoder.transform(unseen_mixed_data['label'])

unseen_mixed_data_labels = unseen_mixed_data['label']

unseen_mixed_data.drop(columns=['label'], inplace=True)

X = data_frame.drop(columns=['label'])

#create y
y = data_frame['label']

#split dataset into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#create classifier or model

#classifier = DecisionTreeClassifier(criterion="entropy")

#classifier = KNeighborsClassifier()

classifier = RandomForestClassifier(criterion="entropy")

#mesure the trauning time
start = time()

classifier.fit(X, y)

feat_importances = pd.Series(classifier.feature_importances_, index=unseen_mixed_data.columns).sort_values(ascending=False)

print(feat_importances)

# feat_importances.plot(kind="barh")

# plt.show()

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