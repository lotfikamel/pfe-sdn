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

dataset_path = '/home/lotfi/pfe/DDOS_datasets/final_datasets/DrDoS_NTP.csv'

#create dataframe
data_frame = pd.read_csv(dataset_path)

encoder = LabelEncoder()

data_frame['label'] = encoder.fit_transform(data_frame['label'])

X = data_frame.drop(columns=['label'])

#create y
y = data_frame['label']

#split dataset into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

#create classifier or model

classifier = DecisionTreeClassifier(criterion="entropy")

# classifier = KNeighborsClassifier()

classifier = RandomForestClassifier(max_features=None)

#mesure the trauning time
start = time()

classifier.fit(X_train, y_train)

feat_importances = pd.Series(classifier.feature_importances_, index=X.columns).sort_values(ascending=False)

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