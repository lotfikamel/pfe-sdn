import pandas as pd
import numpy as np

dataset_path = '/home/lotfi/pfe/DDOS_datasets/DrDoS_UDP.csv'

dataframe = pd.read_csv(dataset_path)

label_counts = dataframe[' Label'].value_counts()

print(f'dataset label counts {label_counts}')