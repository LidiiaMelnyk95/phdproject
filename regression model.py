import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv('/Users/lidiiamelnyk/Downloads/Benchmark_Regression/train_bm.csv')

data.shape
data.head()

data.isnull().sum()

from sklearn.utils import shuffle
data = shuffle(data, random_state=42)
#creating four divisions
div = int(data.shape[0]/4)
#3 parts to train set and 1 part to test
train = data.loc[:3*div+1, :]
test = data.loc[3*div+1 :]
train.head()
test.head()

#storing a simple mean in a new column in a test set as 'simple_mean'
test['simple_mean'] = train['Item_Outlet_Sales'].mean()

#calculating mean absolute error
from sklearn.metrics import mean_absolute_error as MAE
simple_mean_error = MAE(test['Item_Outlet_Sales'], test['simple_mean'])

out_type = pd.pivot_table(train, values = 'Item_Outlet_Sales', index = ['Outlet_Type'], aggfunc= np.mean)
print(out_type)
import re
test['Out_type_mean'] = 0

#for every unique entry in Outlet identifier
for i in train['Outlet_Type'].unique():
    #assign the mean value corresponding to unique entry
    test['Out_type_mean'][test['Outlet_Type'] == str(i)] = train['Item_Outlet_Sales'][train['Outlet_Type'] == str(i)].mean()


out_type_error = MAE(test['Item_Outlet_Sales'], test['Out_type_mean'])

out_year = pd.pivot_table(train, values = 'Item_Outlet_Sales', index = ['Outlet_Establishment_Year'], aggfunc= np.mean)
print(out_year)

test['Out_year_mean'] = 0

for i in train['Outlet_Establishment_Year'].unique():
    test['Out_year_mean'][test['Outlet_Establishment_Year'] == str(i)] = train['Item_Outlet_Sales'][train['Outlet_Establishment_Year']  == str(i)].mean()

out_year_error = MAE(test['Item_Outlet_Sales'], test['Out_year_mean'])
print(out_year_error)

out_loc = pd.pivot_table(train, values = 'Item_Outlet_Sales', index = ['Outlet_Location_Type'], aggfunc= np.mean)
print(out_year)
test['Out_loc_mean'] = 0
for i in train['Outlet_Location_Type'].unique():
    test['Out_loc_mean'][test['Outlet_Location_Type'] == str(i)] = train['Item_Outlet_Sales'][train['Outlet_Location_Type']  == str(i)].mean()

out_loc_error = MAE(test['Item_Outlet_Sales'], test['Out_loc_mean'])
print(out_loc_error)

combo = pd.pivot_table(train, values = 'Item_Outlet_Sales', index = ['Outlet_Establishment_Year','Outlet_Location_Type'], aggfunc= np.mean)
print(combo)

test['Super_mean'] = 0

s2 = 'Outlet_Location_Type'
s1 = 'Outlet_Establishment_Year'

for i in test[s1].unique():
    for j in test[s2].unique():
        test['Super_mean'][(test[s1] == str(i)) & (test[s2] == str(j))] = train['Item_Outlet_Sales'][(train[s1] == i) & (train[s2]==str(j))].mean()


super_mean_error = MAE(test['Item_Outlet_Sales'], test['Super_mean'])
print(super_mean_error)
