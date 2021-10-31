import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
data = pd.read_csv('/Users/lidiiamelnyk/Downloads/KNN Implementation/data_cleaned.csv')
print(data.shape)
print(data.head())

print(data.isnull().sum())
x = data.drop(['Survived'], axis = 1)
y = data['Survived']
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
x = ss.fit_transform(x)

from sklearn.model_selection import train_test_split
train_x,test_x, train_y, test_y = train_test_split(x,y, random_state= 96, stratify = y)

from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.metrics import f1_score

#creating instance of KNN
clf = KNN(n_neighbors=1)

#fitting the model
clf.fit(train_x, train_y)

#predicting over the trained set and calculating f1-score
train_predict = clf.predict(train_x)
k = f1_score(train_predict, train_y)
print('Training F1 score {}'.format(k))

#predicting over the test set and calculating f1-score
test_predict = clf.predict(test_x)
k = f1_score(test_predict, test_y)
print('Testing F1 score {}'.format(k))

def F1score(k):
    #takes an input K consisting of a range of K values for KNN
    # K = list
    #returns: lists containing f1s corresponding to every K value
    #train_f1= list of f1 score for training data
    #train_f2 = list of f2 scores for test data

    train_f1 = []
    test_f1 = []
    for i in k:
        clf = KNN(n_neighbors= i)
        clf.fit(train_x,train_y)
        tmp= clf.predict(train_x)
        tmp = f1_score(tmp, train_y)
        train_f1.append(tmp)

        tmp = clf.predict(test_x)
        tmp = f1_score(tmp, test_y)
        test_f1.append(tmp)
    return train_f1, test_f1

#defining K range
k = range(1, 150)
#calling above defined function
train_f1, test_f1 = F1score(k)
score = pd.DataFrame({'train_score': train_f1, 'test_score': test_f1}, index = k)
print(score.head())

plt.plot(k, test_f1, color = 'red', label = 'test')
plt.plot(k, train_f1, color = 'blue', label = 'train')
plt.xlabel('K Neighbours')
plt.ylabel('F1 score')
plt.title ('F1 Curve')
plt.ylim(0.4, 1)
plt.legend()
plt.show()