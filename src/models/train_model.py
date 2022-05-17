import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
import pickle

def train_and_pickle():
    cols = ['Flow ID', 'Source IP', 'Source Port', 'Destination IP', 'Destination Port', 'Protocol', 'Timestamp',
    'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets','Total Length of Fwd Packets', 'Total Length of Bwd Packets',
    'Fwd Packet Length Max', 'Fwd Packet Length Min','Fwd Packet Length Mean''Fwd Packet Length Std', 'Bwd Packet Length Max',
    'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean',
    'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min',
    'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags',
    'Bwd URG Flags', 'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s', 'Min Packet Length', 'Max Packet Length',
    'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count',
    'PSH Flag Count', 'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Average Packet Size',
    'Avg Fwd Segment Size', 'Avg Bwd Segment Size', 'Fwd Header Length.1', 'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk','Fwd Avg Bulk Rate',
    'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate', 'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets',
    'Subflow Bwd Bytes', 'Init_Win_bytes_forward', 'Init_Win_bytes_backward', 'act_data_pkt_fwd', 'min_seg_size_forward',
    'Active Mean', 'Active Std', 'Active Max', 'Active Min','Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min','SimillarHTTP',
    'Inbound', 'Label']

    dataset = pd.read_csv('../data/interim/training.csv', names = cols, skiprows = 1)
    dataset.drop(['Flow ID', 'Source IP', 'Source Port', 'Destination IP', 'Destination Port', 'Protocol', 'Timestamp','Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'FIN Flag Count', 'PSH Flag Count', 'ECE Flag Count',
                'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk', 
                'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate', 'Flow Bytes/s'], axis = 1, inplace = True)

    dataset['Label'] = dataset['Label'].replace({ 'DrDoS_DNS': 1})
    dataset['Label'] = dataset['Label'].replace({ 'BENIGN': 0})
    xtrain, ytrain = dataset.iloc[:,:-1], dataset['Label']

    data_cleaned_train = [['Fwd Packet Length Max', 'min_seg_size_forward', 'Inbound', 'URG Flag Count', 'Fwd PSH Flags', 'Flow IAT Mean']]
    model = CatBoostClassifier(iterations = 1000, learning_rate = 0.05, eval_metric = 'F1', verbose = False, random_state = 42)
    model.fit(data_cleaned_train, ytrain, verbose=False,  plot=False)

    pickle.dump(model, open('../../models/cb_model.pkl', 'wb'))
