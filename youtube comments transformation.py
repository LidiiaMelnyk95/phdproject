import dateparser as dateparser
import pandas as pd
import timedelta
import datetime as datetime, timedelta
import dateparser

df = pd.read_csv('/Users/lidiiamelnyk/Documents/GitHub/Linguistic_materials/Youtube_comments_tsg(2).csv', sep = ',', encoding = 'utf-8-sig')

for i, row in df.iterrows():
    correct_data = []
    s = row['comment_time']
    try:
        parsed_s = dateparser.parse(s, settings={'RELATIVE_BASE': datetime.datetime(2021, 6, 4)}).strftime('%m/%d/%Y')
        correct_data.append(parsed_s)
    except ValueError:
        correct_data = []
        pass
    df.at[i, 'date'] = correct_data.append(parsed_s)

print(df['date'].head(10))