#import pandas data frame library
import pandas as pd

#import numpy
import numpy as np

udp_lag_dataset_path = '/home/lotfi/pfe/DDOS_datasets/final_datasets/UDPLag.csv'

udp_lag_data_frame = pd.read_csv(udp_lag_dataset_path)

tcp_in_udp = udp_lag_data_frame.loc[udp_lag_data_frame['protocol'] == 17]

tcp_in_udp.to_csv('/home/lotfi/pfe/DDOS_datasets/test/tcp_in_udp.csv', index=False)
