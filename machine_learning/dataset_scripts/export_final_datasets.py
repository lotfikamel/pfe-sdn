#import pandas data frame library
import pandas as pd

#import numpy
import numpy as np

from dataset_attributes import attributes_rename_mapping

udp_lag_dataset_path = '/home/lotfi/pfe/DDOS_datasets/UDPLag.csv'

tcp_syn_dataset_path = '/home/lotfi/pfe/DDOS_datasets/Syn.csv'

udp_lag_data_frame = pd.read_csv(udp_lag_dataset_path)

tcp_syn_data_frame = pd.read_csv(tcp_syn_dataset_path)

attributes = attributes_rename_mapping.keys()

# select custom attr
udp_lag_data_frame = udp_lag_data_frame[attributes]

tcp_syn_data_frame = tcp_syn_data_frame[attributes]

udp_lag_data_frame.rename(columns=attributes_rename_mapping, inplace=True)

tcp_syn_data_frame.rename(columns=attributes_rename_mapping, inplace=True)

print(udp_lag_data_frame['protocol'].value_counts())

print(tcp_syn_data_frame['protocol'].value_counts())

udp_lag_data_frame.to_csv('/home/lotfi/pfe/DDOS_datasets/final_datasets/UDPLag.csv', index=False)

tcp_syn_data_frame.to_csv('/home/lotfi/pfe/DDOS_datasets/final_datasets/TCPSyn.csv', index=False)