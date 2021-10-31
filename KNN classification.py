import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
data = pd.read_csv('/Users/lidiiamelnyk/Downloads/KNN Implementation/data_cleaned.csv')
print(data.shape)
print(data.head())

#separating independent and dependent variables

x = data.drop(['Survived'], axis = 1)
y = data['Survived']
print(x.shape, y.shape)

#importing the MinMax scaler
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
x_scaled = scaler.fit_transform(x)

x = pd.DataFrame(x_scaled, columns = x.columns)
from sklearn.model_selection import train_test_split
train_x, test_x, train_y, test_y = train_test_split(x,y, random_state= 56, stratify=y)

from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.metrics import f1_score

#creating instance of KNN
clf = KNN(n_neighbors= 10)
#fitting the model
clf.fit(train_x, train_y)

#predicting over the train set and calculating F1
test_predict = clf.predict(test_x)
k = f1_score(test_predict, test_y)
print('Test F1 score is {}'.format(k))


#create an elbow curve
def elbow(K):
    #initiating an empty list
    test_error = []
    #training model for every value of K
    for i in K:
        clf = KNN(n_neighbors = i)
        clf.fit(train_x, train_y)
        #appending F1 score to empty list calculated using the prediction
        tmp = clf.predict(test_x)
        tmp = f1_score(tmp, test_y)
        error = 1 - tmp
        test_error.append(error)

    return test_error

#defining K range
k = range(6,20,2)

# calling above defined function
test = elbow(k)

#plotting the curves
plt.plot(k,test)

plt.xlabel('K Neighbours')
plt.ylabel('Test error')
plt.title('Elbow curve for test')
plt.show()

data_train = pd.read_csv('/Users/lidiiamelnyk/Downloads/KNN Implementation/train_cleaned.csv')
print(data_train.shape)
print(data_train.head())
x = data_train.drop(['Item_Outlet_Sales'], axis = 1)
y = data_train['Item_Outlet_Sales']
print(x.shape, y.shape)
from sklearn.neighbors import KNeighborsRegressor as KNR
scaler = MinMaxScaler()
x_scaled = scaler.fit_transform(x)
x = pd.DataFrame(x_scaled)
from sklearn.metrics import mean_squared_error as mse

train_x, test_x, train_y, test_y = train_test_split(x, y, random_state= 56)
reg = KNR(n_neighbors=5)
reg.fit(train_x,train_y)

#predicting over the train set and calculating mse
test_predict = reg.predict(test_x)
k = mse(test_predict, test_y)
print ('Test MSE {}'.format(k))

def elbow_mse(m):
    test_mse_list = []
    for i in m:
        reg = KNR(n_neighbors=i)
        reg.fit(train_x, train_y)
        tmp= reg.predict(train_x)
        tmp = mse(tmp,train_y)
        test_mse_list.append(tmp)

    return test_mse_list

m = range (1, 40)
test = elbow_mse(m)

plt.plot( test, m)
plt.xlabel('K Neighbours')
plt.ylabel('Test Mean Squared Error')
plt.title( 'Elbow Curve for test')
plt.show()