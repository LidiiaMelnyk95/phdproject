import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

data = pd.read_csv('/Users/lidiiamelnyk/Downloads/Benchmark_Classification/train.csv')
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

test['simple_mode'] = train['Survived'].mode()[0]
test['simple_mode'].head()

simple_mode_accuracy = accuracy_score(test['Survived'], test['simple_mode'])
print(simple_mode_accuracy)

gender_mode = pd.crosstab(train['Survived'], train['Sex'])
print(gender_mode)
test['gender_mode'] = test['Survived']
for i in test['Sex'].unique():
    #calculate and assign mode to new column, corresponding to unique values in 'Sex'
    test['gender_mode'][test['Sex'] == str(i)]  = train['Survived'][train['Sex'] == str(i)].mode()[0]

gender_accuracy = accuracy_score(test['Survived'], test['gender_mode'])
print(gender_accuracy)

class_mode = pd.crosstab(train['Survived'], train['Pclass'])
print(class_mode)
test['class_mode'] = test['Survived']


for i in test['Pclass'].unique():
    test['class_mode'][test['Pclass'] == str(i)] = train['Survived'][train['Pclass'] == str(i)].mode()[0]

class_accuracy = accuracy_score(test['Survived'], test['class_mode'])
print(class_accuracy)