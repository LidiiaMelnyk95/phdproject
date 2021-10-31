
from textblob_de import TextBlobDE as TextBlob
import nltk
import glob

import pandas as pd

all_files = glob.glob('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/2020-02/german/*.csv')
li = []
for file in all_files:
    try:
        df1 = pd.read_csv(file, sep = ';', float_precision='round_trip',  index_col=None, header=0)
        li.append(df1)
    except ValueError or AssertionError:
        continue

df = pd.concat(li, axis=0, ignore_index=True)
df['full_text'].drop_duplicates()
result = []
sentiment_scores = []
total_score = []
df['total_score '] = ''
df['full_text'] = df['full_text'].astype(str)

for i, row in df.iterrows():
    for k in row['full_text'].split(' '):
        k = k.replace('https', '')
        result.append(k)


from nltk import word_tokenize
myfile = open('/Users/lidiiamelnyk/Downloads/stop_words_german.txt', "r", encoding = 'utf-8-sig') #upload the stopwords
content = myfile.read()
stopwords_list = content.split("\n")
stopwords_list = [w.lower() for w in stopwords_list]
german_words_all = open('/Users/lidiiamelnyk/Downloads/wordlist-german.txt', "r", encoding = 'utf-8-sig') #upload the stopwords
content = german_words_all.read()
all_german = content.split("\n")
all_german_words = [w.lower() for w in all_german]
new_result= []
for word in result:
    word = word.lower()
    if word in all_german_words:
        if word not in stopwords_list:
            new_result.append(word)

comments = TextBlob(' '.join(new_result))
comments = comments.words.lemmatize()
comments = TextBlob(' '.join(comments))

with open('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/2020-02/german/comments.txt', 'w+') as myfile:
    myfile.write(comments)
    myfile.close()