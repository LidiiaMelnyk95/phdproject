import datetime

import langid
import pandas as pd
import glob

path = '/Users/lidiiamelnyk/Documents/tweets_tsg/' # use your path

df = pd.read_csv('/Users/lidiiamelnyk/Documents/tweets_tsg/tweets_full.csv', sep = ';')
timestamp_list = df['Tweet_Timestamp'].values
df['Tweet_Timestamp'].fillna(method='ffill')
df['Tweet_Timestamp'] = df['Tweet_Timestamp'].astype(str)
for i,row in df.iterrows():
    new_date_array = []
    for d in row['Tweet_Timestamp'].split('\n'):
        new_date = datetime.datetime.fromtimestamp(int(d) / 1000).strftime('%d/%m/%Y')
        new_date_array.append(new_date)
    df.at[i, 'Date'] = new_date_array

df['Tweet_Content'] = df['Tweet_Content'].astype(str)
df['Comment_Content'] = df['Comment_Content'].astype(str)
df['Comment_Name'] = df['Comment_Name'].astype(str)
for i, row in df.iterrows():
    for k in row['Comment_Content'].split('\n'):
        if k == 'undefined':
            pass
        else:
            df.loc[i, 'Tweet_Content'] = k

for i, row in df.iterrows():
    for m in row['Comment_Name'].split('\n'):
        if m == 'undefined':
            pass
        else:
            df.loc[i, 'Author_Name'] = m
import numpy as np

for i, row in df.iterrows():
    counter = 0
    length = []
    row_length =  len(row['Tweet_Content'].split())
    if row_length <= 3:
        df.drop(i, inplace = True)


#df = df.drop_duplicates(subset ="Tweet_Content")

df.dropna(axis = 0, how='any', thresh=None, subset=None, inplace=False)

print(df['Tweet_Content'].count())

new_columns = 'Tweet_Website', 'Tweet_Content', 'Author_Name', 'Date'

df = df.reindex(columns = new_columns)
with open('/Users/lidiiamelnyk/Documents/tweets_tsg/edited.csv', 'w+', encoding='utf-8-sig', newline='') as my_file:
	df.to_csv(my_file, sep=',', na_rep='', float_format=None, columns = new_columns,
			   header=True, index=False, index_label=None,
			   mode='a', compression='infer',
			   quoting=None, quotechar='"', line_terminator=None, chunksize=None,
			   date_format=None, doublequote=True, escapechar=None, decimal='.')
