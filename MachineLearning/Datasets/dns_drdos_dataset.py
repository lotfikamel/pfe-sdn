#import pandas data frame library
import pandas as pd

#import numpy
import numpy as np

#import matplotlib
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression

from sklearn.naive_bayes import GaussianNB as KNN

from sklearn.naive_bayes import GaussianNB as RandomForest

from sklearn.svm import SVC

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

from dataset_attributes import attributes_rename_mapping

attributes = attributes_rename_mapping.keys()

dataset_path = '/home/lotfi/pfe/DDOS_datasets/final_datasets/DrDoS_DNS.csv'

#create dataframe
data_frame = pd.read_csv(dataset_path)

# data_frame = data_frame[attributes]

# data_frame.rename(columns=attributes_rename_mapping, inplace=True)

# data_frame = data_frame.replace([np.inf, -np.inf, np.nan], np.nan).dropna()

# data_frame.drop_duplicates(inplace=True)

encoder = LabelEncoder()

data_frame['label'] = encoder.fit_transform(data_frame['label'])

X = data_frame.drop(columns=['label'])

#create y
y = data_frame['label']

smote = SMOTE()

X_smote, y_smote = smote.fit_sample(X, y)

#split dataset into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#create classifier or model

# classifier = KNeighborsClassifier()

# classifier = RandomForestClassifier(criterion="entropy")

classifier = RandomForest()

#mesure the trauning time
start = time()

classifier.fit(X_train, y_train)

end = time() - start

print(f'training time is : {end}')

predictions = classifier.predict(X_test)

confusion_matrix = metrics.confusion_matrix(y_test, predictions)

classification_report = metrics.classification_report(y_test, predictions, labels=np.unique(y), target_names=encoder.inverse_transform(np.unique(y)))

print('confusion matrix :')

print(confusion_matrix)

print('classification report :')

print(classification_report)
