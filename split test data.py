import numpy as np
import pandas as pd
punctuation = ('.', '…', '?', '!')
df= pd.read_csv('/Users/lidiiamelnyk/Documents/Buts, Duda.csv', sep = ';', encoding='utf-8-sig', usecols= ("Comments", "Label"))


for i, row in df.iterrows():
    df['Comments'] = df['Comments'].astype(str)
    for line in row['Comments'].split('\n'):
        line = line.replace(',', ' ')
        line = line.replace('!', '.')
        line = line.replace('?', '.')
        line = line.replace('…', '.')
        df.at[i,'edited'] = line
df = df.assign(edited=df['edited'].str.split('.')).explode('edited')
new_cols = 'Comments', 'Label','edited'
print(df.head(10))
df = df.reindex(columns = new_cols)
with open('/Users/lidiiamelnyk/Documents/buts_comment_one_sentence.csv', 'w+', newline = '', encoding='utf-8-sig') as file:
    df.to_csv(file, sep=',', na_rep='', float_format=None,
               columns= new_cols,
               header=True, index=False, index_label=None,
               mode='a', compression='infer',
               quoting=None, quotechar='"', line_terminator=None, chunksize=None,
               date_format=str, doublequote=True, escapechar=None, decimal='.', errors='strict')
    file.close()