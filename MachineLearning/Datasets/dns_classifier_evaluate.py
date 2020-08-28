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

#split dataset into train and test
X_train, X_test, y_train, y_test = train_test_split(X_smote, y_smote, test_size=0.2)

#create classifier or model

# classifier = DecisionTreeClassifier(criterion="entropy")

classifier = KNeighborsClassifier()

#classifier = RandomForestClassifier()

#mesure the trauning time
start = time()

classifier.fit(X_train, y_train)

#feat_importances = pd.Series(classifier.feature_importances_, index=X.columns).sort_values(ascending=False)

#feat_importances.plot(kind="barh")

#plt.show()

end = time() - start

print(f'training time is : {end}')

predictions = classifier.predict(X_test)

labels = list(map(int, predictions))

confusion_matrix = metrics.confusion_matrix(y_test, predictions, labels=np.unique(y))

classification_report = metrics.classification_report(y_test, predictions, labels=np.unique(y), target_names=encoder.inverse_transform(np.unique(y)), digits=6)

print('confusion matrix :')

print(confusion_matrix)

print('classification report :')

print(classification_report)

print('accuracy', metrics.accuracy_score(y_test, predictions))