import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
data = pd.read_csv('/Users/lidiiamelnyk/Downloads/Hold_Out/data_cleaned.csv')
print(data.shape)
print(data.head())

print(data.isnull().sum())

data_x = data.drop(['Survived'], axis = 1)
data_y = data['Survived']

from sklearn.model_selection import train_test_split as tts
train1_x, test_x, train1_y, test_y = tts(data_x, data_y, test_size = 0.2, random_state = 51, stratify = data_y)
train_x, val_x, train_y, val_y = tts(train1_x, train1_y, test_size = 0.2, random_state = 51, stratify = train1_y)
print((train_y.value_counts()/len(train_y)))
print((val_y.value_counts()/len(val_y)))
print((test_y.value_counts()/len(test_y)))

