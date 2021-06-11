import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, classification_report


def file2sentences(filename):
    txt = ""
    with open(filename, "r", encoding="utf-8") as f:
        txt = f.read()

        txt = txt.replace("?", ".")
        txt = txt.replace("!", ".")
        txt = txt.replace("»", "")
        txt = txt.replace("«", "")
        txt = txt.replace(":", "")
        txt = txt.replace(";", "")
        txt = txt.replace("...", ".")
        txt = txt.replace("…", ".")
        txt = txt.replace("\n", ".")
        txt = txt.replace("  ", " ")
        txt = txt.replace("\"", "")
        txt = txt.replace("„", "")

        sentences = txt.split(".")
        for i in range(len(sentences)):
            sentences[i] = sentences[i].strip()

        sentences = [x for x in sentences if x != ""]
        return sentences


ukrainian = file2sentences("/Users/lidiiamelnyk/Downloads/articles_no_duplicates.txt")
russian = file2sentences("/Users/lidiiamelnyk/Downloads/articles_russian_no_duplicates.txt")
#surzhyk = file2sentences("/Users/lidiiamelnyk/Downloads/surzhyk.txt")

X = np.array(ukrainian + russian)
y = np.array(['uk'] * len(ukrainian) + ['ru'] * len(russian))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

cnt = CountVectorizer(analyzer='char', ngram_range=(2, 2))

pipeline = Pipeline([('vectorizer', cnt), ('model', MultinomialNB())])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))


import glob

path = '/Users/lidiiamelnyk/Documents/comments_folder/' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, sep = ',', header=0,  encoding='utf-8-sig',
                         float_precision='round_trip')
    li.append(df)

dataframe1 = pd.concat(li, axis=0, ignore_index=True)



spec_chars = ['"',"#","%","&","'","(",")",
              "*","+","/",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–", '$']
for char in spec_chars:
    dataframe1['comment'] = dataframe1['comment'].str.replace(char, ' ')

print (dataframe1['comment'].head())

for i, row in dataframe1.iterrows():
    language = []
    dataframe1['comment'] = dataframe1['comment'].astype(str)
    for line in row['comment'].split(" "):
        line = [line]
        language_pred = pipeline.predict(line)
        language.append(str(language_pred))
    dataframe1.at[i, 'detected_language_array'] = ' '.join(language)

import math

for i, row in dataframe1.iterrows():
    dataframe1['detected_language_array'] = dataframe1['detected_language_array'].astype(str)
    array_from_string = row['detected_language_array'].split(' ')
    all_l2w_count = len(array_from_string)
    ukr_words = row['detected_language_array'].count("['uk']")
    ru_words = row['detected_language_array'].count("['ru']")
    #szk_words = row['detected_language_array'].count("['szh']")
    percentage_ukr = math.ceil((ukr_words / all_l2w_count) * 100) / 100
    percentage_ru = math.ceil((ru_words / all_l2w_count) * 100) / 100
    #percentage_szk = math.ceil((szk_words / all_l2w_count) * 100) / 100
    if percentage_ukr > 0.70:
        dataframe1.at[i, 'predicted_language'] = "Ukrainian"
    elif percentage_ru > 0.70:
        dataframe1.at[i, 'predicted_language'] = "Russian"
    else:
        dataframe1.at[i, 'predicted_language'] = "Ukrainian"
import datetime
dataframe1 = dataframe1.reindex(columns = ['url', 'comment','date','name','readers','predicted_language'])
dataframe1.drop_duplicates()
one_sentence_comments = dataframe1["comment"].str.split('.').apply(pd.Series, 1).stack()
one_sentence_comments.index = dataframe1['comment_new'].index.droplevel(-1)  # to line up with df's index


        # There are blank or emplty cell values after above process. Removing them
one_sentence_comments.replace('', np.nan, inplace=True)
one_sentence_comments.dropna(inplace=True)
one_sentence_comments.name = 'OSC'

del dataframe1['OSC']
dataframe1 = dataframe1.join(one_sentence_comments)
print(dataframe1.head(10))

with open('/Users/lidiiamelnyk/Documents/comments_censor_net.csv', 'w+', newline = '', encoding='utf-8-sig') as file:
    dataframe1.to_csv(file, sep=',', na_rep='', float_format=None,
               columns=['url', 'comment', 'date', 'name','readers','predicted_language'],
               header=True, index=False, index_label=None,
               mode='a', compression='infer',
               quoting=None, quotechar='"', line_terminator=None, chunksize=None,
               date_format=str, doublequote=True, escapechar=None, decimal='.', errors='strict')
    file.close()