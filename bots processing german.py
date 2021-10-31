import matplotlib.pyplot as plt
import seaborn as sns
from textblob_de import TextBlobDE as TextBlob
import nltk
sns.set(color_codes=True)
import glob

import pandas as pd
nltk.download('vader_lexicon')
import numpy as np
from textblob_de import sentiments
all_files = glob.glob('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/2020-02/german/bots/*.csv')
li = []
for file in all_files:
    try:
        df1 = pd.read_csv(file, sep = ',', float_precision='round_trip',  index_col=None, header=0)
        li.append(df1)
    except ValueError or AssertionError:
        continue

df_main = pd.concat(li, axis=0, ignore_index=True)
df_main['full_text'].drop_duplicates()
print(df_main['full_text'].count())
df = df_main[df_main['bot_score'] >= 0.7]
print(df['full_text'].count())
import re
from urllib.parse import urlparse
import collections
url_list = []
df2 = df[df['entities.urls'] == '[]']
print(df2['entities.urls'].count())
for i,row in df.iterrows():
    for k in row['entities.urls'].split(','):
        if len(k) > 5:
            k = re.findall(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+',k)
            url_list.append(k)

url_list = [x for x in url_list if x]
url_list = [x for sublist in url_list for x in sublist]

domain_list = []
for x in url_list:
    domain = urlparse(x).netloc
    if len(domain) > 7:
        domain_list.append(domain)

counter = collections.Counter(domain_list)
print(counter)
