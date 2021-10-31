import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

data = pd.read_csv('/Users/lidiiamelnyk/Downloads/1/titanic_train.csv')
data.shape
print(data.isnull().sum())

#data_row_del = data.dropna(thresh = 500, axis =1)
#print(data_row_del['Age'].head())

#data.shape
#data_row_del.shape

data['Cabin'].fillna(value = 'missing')
data['Age'].fillna(value = 999)

data_replace = data.copy()
data_replace['Age'] = data_replace['Age'].fillna(value = 999)
print(data_replace.isna().sum())

data_replace['Cabin_na'] = (data['Cabin'].isna()).astype('int')
print(data_replace.head())

mean_val = data['Age'].mean()

data_cleaned = data.copy()
data_cleaned['Age'] = data_cleaned['Age'].fillna(value = mean_val)

print(data['Embarked'].value_counts())

mode_val = data['Embarked'].mode()[0]
data_cleaned['Embarked'] = data_cleaned['Embarked'].fillna(value= mode_val)

print(data.corr())
print((data[['Name', 'Age']].loc[(data['Age'].isnull() >0)]).head(20))

categorical_col = ['Name', 'Sex', 'Ticket', 'Cabin']
print(data[categorical_col].nunique())

pd.get_dummies(data['Embarked'].head())
data_cleaned = data_cleaned.drop(['Name', 'Ticket', 'Cabin'], axis = 1)
data_cleaned = pd.get_dummies(data_cleaned)
print(data_cleaned.head())

data['Embarked'] = data['Embarked'].map({'Q':0,'S':1, 'C':2 })

print(data.describe())
Q1 = data['Fare'].quantile(0.25)
Q3 = data['Fare'].quantile(0.75)
IQR = data['Fare'].quantile(0.75) - data['Fare'].quantile(0.25)
whisker_1 = Q1 - (1.5*IQR)
whisker_2 = Q3 + (1.5*IQR)

data_new = data.loc[data['Fare']< whisker_2]
data.shape, data_new.shape
data.loc[data['Fare']<7] = Q1
import matplotlib.pyplot as plt
(data['Fare']).hist()
plt.show()


(np.sqrt(data['Fare'])).hist()
plt.show()