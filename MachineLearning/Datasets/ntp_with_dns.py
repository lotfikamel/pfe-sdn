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

dataset_path = '/home/lotfi/pfe/DDOS_datasets/final_datasets/DrDoS_DNS.csv'

#create dataframe
data_frame = pd.read_csv(dataset_path)

encoder = LabelEncoder()

data_frame['label'] = encoder.fit_transform(data_frame['label'])

X = data_frame.drop(columns=['label'])

#create y
y = data_frame['label']

smote = SMOTE()

X_smote, y_smote = smote.fit_sample(X, y)

classifier = RandomForestClassifier()

classifier.fit(X_smote, y_smote)

ntp_dataset_path = '/home/lotfi/pfe/DDOS_datasets/final_datasets/DrDoS_NTP.csv'

#create dataframe
ntp_dataframe = pd.read_csv(ntp_dataset_path)

X_test = ntp_dataframe.drop(columns=['label'])

y_test = encoder.transform(ntp_dataframe['label'])

predictions = classifier.predict(X_test)

confusion_matrix = metrics.confusion_matrix(y_test, predictions, labels=np.unique(y))

classification_report = metrics.classification_report(y_test, predictions, labels=np.unique(y), target_names=encoder.inverse_transform(np.unique(y)), digits=6)

print('confusion matrix :')

print(confusion_matrix)

print('mesure de perfomance de la classifications des flux NTP avec le Classifieur DNS :')

print(classification_report)

print('accuracy', metrics.accuracy_score(y_test, predictions))