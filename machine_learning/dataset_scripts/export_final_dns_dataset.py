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

dns_reflection_dataset_path = '/home/lotfi/pfe/DDOS_datasets/DrDoS_DNS.csv'

dns_drdos_dataframe = pd.read_csv(dns_reflection_dataset_path, nrows=3500000)

attributes = attributes_rename_mapping.keys()

dns_drdos_dataframe = dns_drdos_dataframe[attributes]

dns_drdos_dataframe.rename(columns=attributes_rename_mapping, inplace=True)

dns_drdos_dataframe = dns_drdos_dataframe.loc[(dns_drdos_dataframe['protocol'] == 17) | (dns_drdos_dataframe['protocol'] == 6)]

dns_drdos_dataframe = dns_drdos_dataframe.loc[(dns_drdos_dataframe['label'] == 'DrDoS_DNS') | (dns_drdos_dataframe['label'] == 'BENIGN')]

dns_drdos_dataframe = clean_dataset(dns_drdos_dataframe)

dns_drdos_dataframe.drop_duplicates(inplace=True)

dns_drdos_benign = dns_drdos_dataframe[dns_drdos_dataframe['label'] == 'BENIGN']

dns_drdos = dns_drdos_dataframe[dns_drdos_dataframe['label'] == 'DrDoS_DNS']

duplicateRowsDF = dns_drdos_dataframe[dns_drdos_dataframe.duplicated()]

print(dns_drdos_dataframe.shape)

print(dns_drdos_dataframe['label'].value_counts())

dns_drdos_dataframe.to_csv('/home/lotfi/pfe/DDOS_datasets/final_datasets/DrDoS_DNS.csv', index=False)

dns_drdos_benign.to_csv('/home/lotfi/pfe/DDOS_datasets/final_datasets/DrDoS_DNS_BENIGN.csv', index=False)

dns_drdos.to_csv('/home/lotfi/pfe/DDOS_datasets/final_datasets/DrDoS_DNS_ONLY.csv', index=False)