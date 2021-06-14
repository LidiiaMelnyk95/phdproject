import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
from ast import literal_eval
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/lidiiamelnyk/Documents/comments_with_names.csv', sep = ',',encoding = 'utf-8-sig')
np.random.seed(42)
df['readers'] = df['readers'].apply(literal_eval)
df = df.join(pd.json_normalize(df['readers']))
df.drop(columns=['readers'], inplace=True)
print(df.describe())

print(df['name'].value_counts().idxmax())
print(df['name'].value_counts().idxmin())
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import mean_absolute_error
import datetime
# retrieve the array
df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
data = df[['date', 'name', 'reading_me', 'i_am_reading']].values

try:
# split into inpiut and output elements
    X, y = data[:, :-1], data[:, -1]
# split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)
# summarize the shape of the training dataset
    print(X_train.shape, y_train.shape)
# identify outliers in the training dataset
    lof = LocalOutlierFactor()
    yhat = lof.fit_predict(X_train)
# select all rows that are not outliers
    mask = yhat != -1
    X_train, y_train = X_train[mask, :], y_train[mask]
# summarize the shape of the updated training dataset
    print(X_train.shape, y_train.shape)
# fit the model
    model = LinearRegression()
    model.fit(X_train, y_train)
# evaluate the model
    yhat = model.predict(X_test)
# evaluate predictions
    mae = mean_absolute_error(y_test, yhat)
    print('MAE: %.3f' % mae)
except KeyError:
    pass