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

def clean_dataset (data_frame) :

		assert isinstance(data_frame, pd.DataFrame)

		data_frame.dropna(inplace=True)

		indices_to_keep = ~data_frame.isin([np.nan, np.inf, -np.inf]).any(1)

		data_frame = data_frame[indices_to_keep].astype(np.float64)

		return data_frame

balanced_udp_dataset_path = '/home/lotfi/pfe/DDOS_datasets/UDPLag/BALANCED_UDP.csv'

balanced_udp_data_frame = pd.read_csv(balanced_udp_dataset_path)

balanced_tcp_dataset_path = '/home/lotfi/pfe/DDOS_datasets/TCPSyn/BALANCED_TCP.csv'

balanced_tcp_data_frame = pd.read_csv(balanced_tcp_dataset_path)

balanced_udp_tcp = pd.concat(objs=[balanced_udp_data_frame, balanced_tcp_data_frame], join='inner')

balanced_udp_tcp.to_csv('/home/lotfi/pfe/DDOS_datasets/TCP_UDP/UDP_TCP.csv', index=False)

balanced_udp_tcp = pd.read_csv('/home/lotfi/pfe/DDOS_datasets/TCP_UDP/UDP_TCP.csv')

encoder = LabelEncoder()

balanced_udp_tcp[' Label'] = encoder.fit_transform(balanced_udp_tcp[' Label'])

balanced_udp_tcp = clean_dataset(balanced_udp_tcp)

balanced_udp_tcp = balanced_udp_tcp.reindex(np.random.permutation(balanced_udp_tcp.index))

balanced_udp_tcp[' Fwd Header Length'] = balanced_udp_tcp[' Fwd Header Length'].abs()

X = balanced_udp_tcp.drop(columns=[' Label'])

print(X.head(50))

#create y
y = balanced_udp_tcp[' Label']

#split dataset into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

#create classifier or model

classifier = DecisionTreeClassifier(criterion="entropy")

#classifier = KNeighborsClassifier()

classifier = RandomForestClassifier(criterion="entropy")

#mesure the trauning time
start = time()

classifier.fit(X_train, y_train)

feat_importances = pd.Series(classifier.feature_importances_, index=X_test.columns).sort_values(ascending=False)

feat_importances.plot(kind="barh")

plt.show()

end = time() - start

print(f'training time is : {end}')

predictions = classifier.predict(X_test)

labels = list(map(int, predictions))

confusion_matrix = metrics.confusion_matrix(y_test, predictions)

classification_report = metrics.classification_report(y_test, predictions, labels=np.unique(y))

print('confusion matrix :')

print(confusion_matrix)

print('classification report :')

print(classification_report)