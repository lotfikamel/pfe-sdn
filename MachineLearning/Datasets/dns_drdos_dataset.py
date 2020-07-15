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

from imblearn.over_sampling import SMOTE

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

dataset_path = '/home/lotfi/pfe/DDOS_datasets/final_datasets/DrDoS_DNS.csv'

#create dataframe
data_frame = pd.read_csv(dataset_path)

dns_benign = data_frame.loc[data_frame['label'] == 'BENIGN']

print(dns_benign['flow_packets_per_seconds'].value_counts())

unseen_dns_benign = dns_benign.iloc[1900:1966,:]

dns_benign = dns_benign.iloc[:1900]

dns_drdos = data_frame.loc[data_frame['label'] == 'DrDoS_DNS']

unseen_dns_drdos = dns_drdos.iloc[10000:11000,:]

dns_drdos = dns_drdos.iloc[:10000]

data_frame = pd.concat(objs=[dns_benign, dns_drdos], join='inner')

data_frame = data_frame.reindex(np.random.permutation(data_frame.index))

encoder = LabelEncoder()

data_frame['label'] = encoder.fit_transform(data_frame['label'])

print(data_frame.head())

unseen_data = pd.concat(objs=[unseen_dns_benign, unseen_dns_drdos], join='inner')

unseen_data = unseen_data.reindex(np.random.permutation(unseen_data.index))

unseen_data['label'] = encoder.transform(unseen_data['label'])

X = data_frame.drop(columns=['label'])

#create y
y = data_frame['label']

smote = SMOTE()

X_smote, y_smote = smote.fit_sample(X, y)

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

classifier.fit(X_smote, y_smote)

print(X.shape, X_smote.shape)

feat_importances = pd.Series(classifier.feature_importances_, index=X.columns).sort_values(ascending=False)

feat_importances.plot(kind="barh")

plt.show()

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