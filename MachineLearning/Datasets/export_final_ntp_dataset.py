#import pandas data frame library
import pandas as pd

#import numpy
import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

from dataset_attributes import attributes_rename_mapping

####
# Clean the data frame
# @return {DataFrame}
###
def clean_dataset (data_frame) :

	data_frame = data_frame.replace([np.inf, -np.inf], np.nan).dropna()

	return data_frame

attributes = attributes_rename_mapping.keys()

ntp_reflection_dataset_path = '/home/lotfi/pfe/DDOS_datasets/DrDoS_NTP.csv'

ntp_drdos_dataframe = pd.read_csv(ntp_reflection_dataset_path)

ntp_drdos_dataframe = ntp_drdos_dataframe[attributes]

print(ntp_drdos_dataframe.shape)

ntp_drdos_dataframe.rename(columns=attributes_rename_mapping, inplace=True)

ntp_drdos_dataframe = ntp_drdos_dataframe.loc[ntp_drdos_dataframe['protocol'] == 17]

ntp_drdos_dataframe = ntp_drdos_dataframe.loc[(ntp_drdos_dataframe['label'] == 'DrDoS_NTP') | (ntp_drdos_dataframe['label'] == 'BENIGN')]

ntp_drdos_dataframe = clean_dataset(ntp_drdos_dataframe)

ntp_drdos_dataframe.drop_duplicates(inplace=True)

ntp_drdos_benign = ntp_drdos_dataframe[ntp_drdos_dataframe['label'] == 'BENIGN']

ntp_drdos = ntp_drdos_dataframe[ntp_drdos_dataframe['label'] == 'DrDoS_NTP']

print(ntp_drdos_dataframe.shape)

print(ntp_drdos_dataframe['label'].value_counts())

ntp_drdos_dataframe.to_csv('/home/lotfi/pfe/DDOS_datasets/final_datasets/DrDoS_NTP.csv', index=False)

ntp_drdos_benign.to_csv('/home/lotfi/pfe/DDOS_datasets/final_datasets/DrDoS_NTP_BENIGN.csv', index=False)

ntp_drdos.to_csv('/home/lotfi/pfe/DDOS_datasets/final_datasets/DrDoS_NTP_ONLY.csv', index=False)