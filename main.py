import numpy as np
import pandas as pd
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


X = np.array(ukrainian + russian)
y = np.array(['uk'] * len(ukrainian) + ['ru'] * len(russian))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

cnt = CountVectorizer(analyzer='char', ngram_range=(2, 2))

pipeline = Pipeline([('vectorizer', cnt), ('model', MultinomialNB())])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))



dataframe1 = pd.read_csv('/Users/lidiiamelnyk/Documents/korrespondent/all_comments.csv', sep = ',', encoding = 'utf-8-sig')
print(dataframe1['comment'].count())
dataframe1 = dataframe1.drop_duplicates(subset=['url', 'comment', 'edited', 'date'], keep='last', inplace=False)
print(dataframe1['edited'].count())
import math
for i, row in dataframe1.iterrows():
    language = []
    dataframe1['comment'] = dataframe1['comment'].astype(str)
    for line in row['comment'].split(" "):
        line = [line]
        language_pred = pipeline.predict(line)
        language.append(str(language_pred))
    dataframe1.at[i, 'detected_language_array'] = ' '.join(language)

for i, row in dataframe1.iterrows():
    language = []
    dataframe1['comment'] = dataframe1['comment'].astype(str)
    for line in row['comment'].split(" "):
        line = [line]
        language_pred = pipeline.predict(line)
        language.append(str(language_pred))
    dataframe1.at[i, 'detected_language_array'] = ' '.join(language)
    dataframe1['detected_language_array'] = dataframe1['detected_language_array'].astype(str)
    array_from_string = row['detected_language_array'].split(' ')
    all_l2w_count = len(array_from_string)
    ukr_words = row['detected_language_array'].count("['uk']")
    ru_words = row['detected_language_array'].count("['ru']")
    percentage_ukr = math.ceil((ukr_words / all_l2w_count) * 100) / 100
    percentage_ru = math.ceil((ru_words / all_l2w_count) * 100) / 100
    print(percentage_ru)
    if percentage_ukr > 0.70:
        dataframe1.at[i, 'predicted_language'] = "Ukrainian"
    elif percentage_ru > 0.70:
        dataframe1.at[i, 'predicted_language'] = "Russian"
    else:
        dataframe1.at[i, 'predicted_language'] = "Ukrainian"

dataframe1 = dataframe1.reindex(columns = ['url', 'comment','date','name','predicted_language'])



with open('/Users/lidiiamelnyk/Documents/korrespondent/all_comments_edited.csv', 'w+', newline = '', encoding='utf-8-sig') as file:
    dataframe1.to_csv(file, sep=',', na_rep='', float_format=None,
               columns=['url', 'comment', 'date', 'name','predicted_language'],
               header=True, index=False, index_label=None,
               mode='a', compression='infer',
               quoting=None, quotechar='"', line_terminator=None, chunksize=None,
               date_format=str, doublequote=True, escapechar=None, decimal='.', errors='strict')
    file.close()


