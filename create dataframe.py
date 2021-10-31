import glob
import pandas as pd

path = '/Users/lidiiamelnyk/Documents/comments_folder/' # use your path
all_files = sorted(glob.glob(path + "/*.csv"))
li = []
for file in all_files:
    try:
        df = pd.read_csv(file, sep= ',')
        li.append(df)
    except ValueError and ConnectionError:
        pass

dataframe1 = pd.concat(li, axis=0, ignore_index=True)
#dataframe1 = dataframe1.reindex(columns = ['tweet_text', 'user_name', 'user_id', 'date', 'language', 'tweet_id'])
dataframe1 = dataframe1.reindex(columns = ['url', 'comment', 'date', 'name'])
print(dataframe1['comment'].count())
dataframe1 = dataframe1.drop_duplicates()
print(dataframe1['comment'].count())

#dataframe1['tweet_text'] = dataframe1['tweet_text'].astype(str)
dataframe1['comment'] = dataframe1['comment'].astype(str)
for i, row in dataframe1.iterrows():
    for line in row['comment'].split('\n'):
        line = line.replace(',', ' ')
        line = line.replace('!', '.')
        line = line.replace('?', '.')
        line = line.replace('…', '.')
        dataframe1.at[i,'edited'] = line
dataframe1 = dataframe1.assign(edited=dataframe1['edited'].str.split('.')).explode('edited')
print(dataframe1['edited'].count())
#dataframe1 = dataframe1.reindex(columns = ['tweet_text', 'user_name', 'user_id', 'date', 'language', 'tweet_id'])
#dataframe1 = dataframe1.reindex(columns = ['url', 'comment', 'edited', 'date', 'name'])
dataframe1 = dataframe1.dropna(axis = 0, how = 'any', thresh = None, subset = None, inplace = False)

with open('/Users/lidiiamelnyk/Documents/comments_folder/all_comments.csv', 'w+', newline = '', encoding='utf-8-sig') as file:
    dataframe1.to_csv(file, sep=',', na_rep='', float_format=None,
               columns=['url', 'comment', 'date', 'name'],
               header=True, index=False, index_label=None,
               mode='a', compression='infer',
               quoting=None, quotechar='"', line_terminator=None, chunksize=None,
               date_format=str, doublequote=True, escapechar=None, decimal='.', errors='strict')
    file.close()
