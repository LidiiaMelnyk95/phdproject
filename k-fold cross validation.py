import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
data = pd.read_csv('/Users/lidiiamelnyk/Downloads/Hold_Out/data_cleaned.csv')
print(data.shape)
print(data.head())

x = data.drop(['Survived'], axis = 1)
y = data['Survived']

from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
x = ss.fit_transform(x)

from sklearn.model_selection import train_test_split
train_x, test_x, train_y, test_y = train_test_split(x, y, random_state= 96, stratify = y)

#importing KNN classifier and metric f-1 score
from sklearn.neighbors import KNeighborsClassifier as KNN

from sklearn.model_selection import cross_val_score
#apply the model (KNN), set samples, number of validation sets to 10 (cross-validation)
score = cross_val_score(KNN(n_neighbors=3), X = train_x, y = train_y, cv = 10 )
print(score)

# consistency using the mean and standard devitation in percentage
print(score.mean() * 100, score.std()* 100)

#automating the process of cross validation for KNNneighbors
def Val_score(n_neighbors):
    '''

    :param n_neighbors: takes n_neighbors as input
    :return:Mean and Standard deviation for each value of n_neighbors
    '''
    avg = []
    std = []

    for i in n_neighbors:
        #10-fold cross validation for every value in n_neighbors
        score = cross_val_score(KNN(n_neighbors = i), X = train_x, y = train_y, cv = 10)

        #adding mean to avg list
        avg.append(score.mean())

        #adding std to std list
        std.append(score.std())

    return avg, std

n_neighbors = range(1, 50)
mean, std = Val_score(n_neighbors)

plt.plot(n_neighbors[10:20], mean [10:20], color = 'red', label = 'red')
plt.xlabel('n_neighbors')
plt.ylabel('mean')
plt.title ('Mean Validation Score')
plt.show()

plt.plot(n_neighbors[10:20], std[10:20], color = 'green', label = 'green')
plt.xlabel('n_neighbors')
plt.ylabel('magnitude')
plt.title ('Mean Standard Deviation')
plt.show()

#checking on unseen data
clf = KNN(n_neighbors= 14)
clf.fit(train_x, train_y)
score_1 = clf.score(train_x, train_y)
score_2 = clf.score(test_x, test_y)
print(score_1, score_2)
