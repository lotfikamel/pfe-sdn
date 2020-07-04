#import pandas data frame library
import pandas as pd

#import numpy
import numpy as np

from dataset_attributes import attributes_rename_mapping

####
# Clean the data frame
# @return {DataFrame}
###
def clean_dataset (data_frame) :

	data_frame = data_frame.replace([np.inf, -np.inf], np.nan).dropna()

	return data_frame

udp_lag_dataset_path = '/home/lotfi/pfe/DDOS_datasets/UDPLag.csv'

tcp_syn_dataset_path = '/home/lotfi/pfe/DDOS_datasets/Syn.csv'

udp_lag_data_frame = pd.read_csv(udp_lag_dataset_path)

tcp_syn_data_frame = pd.read_csv(tcp_syn_dataset_path)

attributes = attributes_rename_mapping.keys()

udp_lag_data_frame = udp_lag_data_frame[attributes]

tcp_syn_data_frame = tcp_syn_data_frame[attributes]

udp_lag_data_frame.rename(columns=attributes_rename_mapping, inplace=True)

tcp_syn_data_frame.rename(columns=attributes_rename_mapping, inplace=True)

udp_lag_data_frame = udp_lag_data_frame.loc[udp_lag_data_frame['protocol'] == 17]

udp_lag_data_frame = udp_lag_data_frame.loc[(udp_lag_data_frame['label'] == 'UDP-lag') | (udp_lag_data_frame['label'] == 'BENIGN')]

udp_lag_data_frame = clean_dataset(udp_lag_data_frame)

tcp_syn_data_frame = tcp_syn_data_frame.loc[tcp_syn_data_frame['protocol'] == 6]

tcp_syn_data_frame = tcp_syn_data_frame.loc[(tcp_syn_data_frame['label'] == 'Syn') | (tcp_syn_data_frame['label'] == 'BENIGN')]

tcp_syn_data_frame = clean_dataset(tcp_syn_data_frame)

udp_lag_data_frame.drop_duplicates(inplace=True)

tcp_syn_data_frame.drop_duplicates(inplace=True)

duplicateRowsDF = udp_lag_data_frame[udp_lag_data_frame.duplicated()]

udp_lag_data_frame.to_csv('/home/lotfi/pfe/DDOS_datasets/final_datasets/UDPLag.csv', index=False)

tcp_syn_data_frame.to_csv('/home/lotfi/pfe/DDOS_datasets/final_datasets/TCPSyn.csv', index=False)