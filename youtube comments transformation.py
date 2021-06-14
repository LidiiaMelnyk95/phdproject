import dateparser as dateparser
import pandas as pd
import timedelta
import datetime as datetime, timedelta
import dateparser

df = pd.read_csv('/Users/lidiiamelnyk/Documents/GitHub/Linguistic_materials/Youtube_comments_tsg(2).csv', sep = ',', encoding = 'utf-8-sig')

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
    length = []
    counter = 0
    row_length =  row['content'].split( )
    for i in row_length:
        counter = counter + 1
        length.append(counter)
    df.at[i, 'comment_length'] = length
    for l in row['comment_length']:
        if l < 3:
            df.drop(row)

print(df['content'].count())