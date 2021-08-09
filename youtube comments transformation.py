import dateparser as dateparser
import pandas as pd
import timedelta
import datetime as datetime, timedelta
import dateparser

df = pd.read_csv('/Users/lidiiamelnyk/Documents/tweets_tsg/Youtube .csv', sep = ';')

for i, row in df.iterrows():
    correct_data = []
    s = row['comment_time']
    s = s.replace('(edited)','').strip('')
    if s is None:
        pass
    parsed_s = dateparser.parse(s, settings={'RELATIVE_BASE': datetime.datetime(2021, 6, 4)}).strftime('%m/%d/%Y')
    correct_data.append(parsed_s)
    df.at[i, 'date'] = correct_data

print(df['content'].count())
print(df['date'].head(10))

df.drop_duplicates(subset ="content")

for i, row in df.iterrows():
    counter = 0
    length = []
    row_length =  len(row['content'].split())
    if row_length <= 3:
        df.drop(i, inplace = True)


print(df['content'].count())

new_columns = 'vedio_url', 'comment_user', 'content', 'date'
df.reindex(columns = new_columns)
with open('/Users/lidiiamelnyk/Documents/tweets_tsg/youtube_corrected.csv', 'w+', newline = '', encoding='utf-8-sig') as file:
    df.to_csv(file, sep=';', na_rep='', float_format=None,
               columns= new_columns,
               header=True, index=False, index_label=None,
               mode='a', compression='infer',
               quoting=None, quotechar='"', line_terminator=None, chunksize=None,
               date_format=str, doublequote=True, escapechar=None, decimal='.', errors='strict')
    file.close()
