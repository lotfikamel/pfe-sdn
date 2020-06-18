import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from datetime import datetime, date
import joblib

dataset_path = '/root/Downloads/ML-Training/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv'

ddos_dataset = pd.read_csv(dataset_path)

# print(ddos_dataset.info())

attack_label = LabelEncoder()

ddos_dataset[' Label'] = attack_label.fit_transform(ddos_dataset[' Label'])

# print(ddos_dataset[' Label'].value_counts())

# sns.countplot(ddos_dataset[' Label'])

# plt.show()

start = datetime.now().replace(microsecond=0)

#####
## Clean the dataset from the big values
## @param {DataFrame} data_frame
## @return {DataFrame}
####
def clean_dataset (data_frame):

	assert isinstance(data_frame, pd.DataFrame)

	data_frame.dropna(inplace=True)

	indices_to_keep = ~data_frame.isin([np.nan, np.inf, -np.inf]).any(1)

	return data_frame[indices_to_keep].astype(np.float64)

####
## Persiste the given classfier
## @param {Object} classifier
## @return {Void}
###
def persiste_classifier (classifier) :

	joblib.dump(classifier, f'{classifier.__class__.__name__}.joblib')

####
## Persiste the given scaler
## @param {Object} scaler
## @return {Void}
###
def persiste_scaler (scaler) :

	joblib.dump(scaler, f'{scaler.__class__.__name__}.joblib')

ddos_dataset = clean_dataset(ddos_dataset)

X = ddos_dataset.drop(' Label', axis=1)

scaler = MinMaxScaler()

X = scaler.fit_transform(X)

y = ddos_dataset[' Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=  0.2)

classifier = RandomForestClassifier()

classifier.fit(X_train, y_train)

persiste_classifier(classifier)

persiste_scaler(scaler)
   
prediction = classifier.predict(X_test)

end = datetime.now().replace(microsecond=0)

duration = end - start

print('timing : {} '.format(duration))

print(classification_report(y_test, prediction))


