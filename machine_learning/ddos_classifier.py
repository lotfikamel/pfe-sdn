import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from datetime import datetime, date

dataset_path = '/root/Downloads/ML-Training/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv'

ddos_dataset = pd.read_csv(dataset_path)

# print(ddos_dataset.info())

'''
RangeIndex: 225745 entries, 0 to 225744
Data columns (total 79 columns):
 #   Column                        Non-Null Count   Dtype  
---  ------                        --------------   -----  
 0    Destination Port             225745 non-null  int64  
 1    Flow Duration                225745 non-null  int64  
 2    Total Fwd Packets            225745 non-null  int64  
 3    Total Backward Packets       225745 non-null  int64  
 4   Total Length of Fwd Packets   225745 non-null  int64  
 5    Total Length of Bwd Packets  225745 non-null  int64  
 6    Fwd Packet Length Max        225745 non-null  int64  
 7    Fwd Packet Length Min        225745 non-null  int64  
 8    Fwd Packet Length Mean       225745 non-null  float64
 9    Fwd Packet Length Std        225745 non-null  float64
 10  Bwd Packet Length Max         225745 non-null  int64  
 11   Bwd Packet Length Min        225745 non-null  int64  
 12   Bwd Packet Length Mean       225745 non-null  float64
 13   Bwd Packet Length Std        225745 non-null  float64
 14  Flow Bytes/s                  225741 non-null  float64
 15   Flow Packets/s               225745 non-null  float64
 16   Flow IAT Mean                225745 non-null  float64
 17   Flow IAT Std                 225745 non-null  float64
 18   Flow IAT Max                 225745 non-null  int64  
 19   Flow IAT Min                 225745 non-null  int64  
 20  Fwd IAT Total                 225745 non-null  int64  
 21   Fwd IAT Mean                 225745 non-null  float64
 22   Fwd IAT Std                  225745 non-null  float64
 23   Fwd IAT Max                  225745 non-null  int64  
 24   Fwd IAT Min                  225745 non-null  int64  
 25  Bwd IAT Total                 225745 non-null  int64  
 26   Bwd IAT Mean                 225745 non-null  float64
 27   Bwd IAT Std                  225745 non-null  float64
 28   Bwd IAT Max                  225745 non-null  int64  
 29   Bwd IAT Min                  225745 non-null  int64  
 30  Fwd PSH Flags                 225745 non-null  int64  
 31   Bwd PSH Flags                225745 non-null  int64  
 32   Fwd URG Flags                225745 non-null  int64  
 33   Bwd URG Flags                225745 non-null  int64  
 34   Fwd Header Length            225745 non-null  int64  
 35   Bwd Header Length            225745 non-null  int64  
 36  Fwd Packets/s                 225745 non-null  float64
 37   Bwd Packets/s                225745 non-null  float64
 38   Min Packet Length            225745 non-null  int64  
 39   Max Packet Length            225745 non-null  int64  
 40   Packet Length Mean           225745 non-null  float64
 41   Packet Length Std            225745 non-null  float64
 42   Packet Length Variance       225745 non-null  float64
 43  FIN Flag Count                225745 non-null  int64  
 44   SYN Flag Count               225745 non-null  int64  
 45   RST Flag Count               225745 non-null  int64  
 46   PSH Flag Count               225745 non-null  int64  
 47   ACK Flag Count               225745 non-null  int64  
 48   URG Flag Count               225745 non-null  int64  
 49   CWE Flag Count               225745 non-null  int64  
 50   ECE Flag Count               225745 non-null  int64  
 51   Down/Up Ratio                225745 non-null  int64  
 52   Average Packet Size          225745 non-null  float64
 53   Avg Fwd Segment Size         225745 non-null  float64
 54   Avg Bwd Segment Size         225745 non-null  float64
 55   Fwd Header Length.1          225745 non-null  int64  
 56  Fwd Avg Bytes/Bulk            225745 non-null  int64  
 57   Fwd Avg Packets/Bulk         225745 non-null  int64  
 58   Fwd Avg Bulk Rate            225745 non-null  int64  
 59   Bwd Avg Bytes/Bulk           225745 non-null  int64  
 60   Bwd Avg Packets/Bulk         225745 non-null  int64  
 61  Bwd Avg Bulk Rate             225745 non-null  int64  
 62  Subflow Fwd Packets           225745 non-null  int64  
 63   Subflow Fwd Bytes            225745 non-null  int64  
 64   Subflow Bwd Packets          225745 non-null  int64  
 65   Subflow Bwd Bytes            225745 non-null  int64  
 66  Init_Win_bytes_forward        225745 non-null  int64  
 67   Init_Win_bytes_backward      225745 non-null  int64  
 68   act_data_pkt_fwd             225745 non-null  int64  
 69   min_seg_size_forward         225745 non-null  int64  
 70  Active Mean                   225745 non-null  float64
 71   Active Std                   225745 non-null  float64
 72   Active Max                   225745 non-null  int64  
 73   Active Min                   225745 non-null  int64  
 74  Idle Mean                     225745 non-null  float64
 75   Idle Std                     225745 non-null  float64
 76   Idle Max                     225745 non-null  int64  
 77   Idle Min                     225745 non-null  int64  
 78   Label                        225745 non-null  object 
dtypes: float64(24), int64(54), object(1)
memory usage: 136.1+ MB
'''

# print(ddos_dataset.isnull().sum())

attack_label = LabelEncoder()

ddos_dataset[' Label'] = attack_label.fit_transform(ddos_dataset[' Label'])

# print(ddos_dataset[' Label'].value_counts())

'''
DDoS      128027
BENIGN     97718
Name:  Label, dtype: int64
'''

# sns.countplot(ddos_dataset[' Label'])

# plt.show()

start = datetime.now().replace(microsecond=0)

def clean_dataset(data_frame):

    assert isinstance(data_frame, pd.DataFrame)

    data_frame.dropna(inplace=True)

    indices_to_keep = ~data_frame.isin([np.nan, np.inf, -np.inf]).any(1)

    return data_frame[indices_to_keep].astype(np.float64)

ddos_dataset = clean_dataset(ddos_dataset)


x = ddos_dataset.drop(' Label', axis=1)

scaler = MinMaxScaler()

x = scaler.fit_transform(x)

y = ddos_dataset[' Label']



x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=  0.2, random_state=42)




random_forest = RandomForestClassifier()

random_forest.fit(x_train, y_train)
   
random_forest_prediction = random_forest.predict(x_test)

'''
timing : 0:01:17  
              precision    recall  f1-score   support

         0.0       1.00      1.00      1.00     19419
         1.0       1.00      1.00      1.00     25724

    accuracy                           1.00     45143
   macro avg       1.00      1.00      1.00     45143
weighted avg       1.00      1.00      1.00     45143

'''  
end = datetime.now().replace(microsecond=0)

duration = end - start
print('timing : {} '.format(duration))

print(classification_report(y_test, random_forest_prediction))


