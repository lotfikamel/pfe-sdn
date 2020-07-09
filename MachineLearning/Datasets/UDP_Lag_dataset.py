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
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier

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

dataset_path = '/home/lotfi/pfe/DDOS_datasets/final_datasets/UDPLag.csv'

#create dataframe
data_frame = pd.read_csv(dataset_path)

udp_benign = data_frame.loc[data_frame['label'] == 'BENIGN']

unseen_udp_benign = udp_benign.iloc[201:700,:]

udp_benign = udp_benign.iloc[:200]

udp_lag = data_frame.loc[data_frame['label'] == 'UDP-lag']

unseen_udp_lag = udp_lag.iloc[201:700,:]

udp_lag = udp_lag.iloc[:200]

data_frame = pd.concat(objs=[udp_benign, udp_lag], join='inner')

data_frame = data_frame.reindex(np.random.permutation(data_frame.index))

print(data_frame.head())

encoder = LabelEncoder()

data_frame['label'] = encoder.fit_transform(data_frame['label'])

print(data_frame.head())

unseen_data = pd.concat(objs=[unseen_udp_benign, unseen_udp_lag], join='inner')

unseen_data = unseen_data.reindex(np.random.permutation(unseen_data.index))

print(unseen_data.head())

unseen_data['label'] = encoder.transform(unseen_data['label'])

print(unseen_data.head())

print(unseen_data.head())

X = data_frame.drop(columns=['label'])

#create y
y = data_frame['label']

X_unseen = unseen_data.drop(columns=['label'])

#create y
y_unseen = unseen_data['label']

#split dataset into train and test
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)

#create classifier or model

classifier = DecisionTreeClassifier(criterion="entropy")

#classifier = KNeighborsClassifier()

classifier = RandomForestClassifier(criterion="entropy")

#mesure the trauning time
start = time()

classifier.fit(X, y)

# feat_importances = pd.Series(classifier.feature_importances_, index=X.columns).sort_values(ascending=False)

# feat_importances.plot(kind="barh")

# plt.show()

end = time() - start

print(f'training time is : {end}')

predictions = classifier.predict(X_unseen)

labels = list(map(int, predictions))

confusion_matrix = metrics.confusion_matrix(y_unseen, predictions)

classification_report = metrics.classification_report(y_unseen, predictions, labels=np.unique(y))

print('confusion matrix :')

print(confusion_matrix)

print('classification report :')

print(classification_report)