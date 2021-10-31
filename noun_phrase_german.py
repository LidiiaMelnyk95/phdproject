import glob

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from textblob_de import TextBlobDE as TextBlob
import re

sns.set(color_codes=True)

nltk.download('vader_lexicon')
nltk.download('punkt')

def get_files_data():
    all_files = glob.glob('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/2020-02/german/bots/*.csv')
    li = []
    for file in all_files:
        try:
            df1 = pd.read_csv(file, sep=',', float_precision='round_trip', index_col=None, header=0)
            li.append(df1)
        except ValueError or AssertionError:
            continue
    return li


def get_main_dataframe():
    df = pd.concat(get_files_data(), axis=0, ignore_index=True)
    with open('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/german_df.csv', 'w+', newline='',
              encoding='utf-8-sig') as file:
        df.to_csv(file, sep=',', na_rep='', float_format=None,
                     header=True, index=False, index_label=None, mode='a', compression='infer',
                     quoting=None, quotechar='"', line_terminator=None, chunksize=None,
                     doublequote=True, escapechar=None, decimal='.', errors='strict')
        file.close()
    return df


def get_text_block():
    df_main = get_main_dataframe()
    df = df_main[df_main['bot_score'] >= 0.5]
    df['full_text'].drop_duplicates()

    result = []
    df['full_text'] = df['full_text'].astype(str)
    # clean the tweets, but currently considering just leaving meaningful POS with stanza so that it is not there at all.
    # run with stanza over tweets and get noun phrases

    for i, row in df.iterrows():
        for k_item in row['full_text'].split(' '):
            k_item = k_item.replace('https', '')
            result.append(k_item)
    return result


myfile = open('/Users/lidiiamelnyk/Downloads/stop_words_german.txt', "r", encoding='utf-8-sig')  # upload the stopwords
content = myfile.read()
stopwords_list = content.split("\n")
stopwords_list = [w.lower() for w in stopwords_list]
stopwords_list = set(stopwords_list)
german_words_all = open('/Users/lidiiamelnyk/Downloads/wordlist-german.txt', "r",
                        encoding='utf-8-sig')  # upload the stopwords
content = german_words_all.read()
all_german = content.split("\n")

all_german_words = [w.lower() for w in all_german]
all_german_words = set(all_german_words)

result = [w.lower() for w in get_text_block() if w not in stopwords_list and w in all_german_words]
comments = TextBlob(' '.join(result))
comments = re.sub(r"(?:\@|https?\://)\S+|\n+", "", str(comments))
comments = TextBlob(comments)
#comments = comments.words.lemmatize()
#comments = TextBlob(' '.join(comments))
sentiment_scores = []
# Check sentiment polarity of each sentence.


cleaned = []
for phrase in comments.noun_phrases:
    count = 0
    splitted_phrase = phrase.split()
    for word in splitted_phrase:
        # Count the number of small words and words without an English definition
        if len(word) <= 2 and word not in all_german_words:
            count += 1
    # Only if the 'nonsensical' or short words DO NOT make up more than 40% (arbitrary) of the phrase add
    # it to the cleaned list, effectively pruning the ones not added.
    if count < len(splitted_phrase) * 0.2:
        cleaned.append(phrase)

print("After compactness pruning:\nFeature Size:", len(cleaned))

cleaned_up = cleaned

noun_phrases = cleaned_up #comments.noun_phrases

for phrase in noun_phrases:
    match = []
    word_match = []
    for word in phrase.split():
        # Find common words among all phrases
        word_match = [p for p in noun_phrases if word not in word_match]
        # If the size of matched phrases set is smaller than 30% of the cleaned phrases,
        # then consider the phrase as non-redundant.
        if len(word_match) <= (len(noun_phrases) * 0.3):
            match.append(word_match)
    # phrase = ' '.join(temp)
    #     print("Match for " + phrase + ": " + str(match))

    if len(match) >= (len(noun_phrases) * 0.1):
        # Redundant feature set, since it contains more than 10% of the number of phrases.
        # Prune all matched features.
        for feature in match:
            if feature in noun_phrases:
                noun_phrases.remove(feature)

        # Add largest length phrase as feature
        noun_phrases.append(max(match, key=len))

cleaned = noun_phrases
print("After redundancy pruning:\nFeature Size:" + str(len(cleaned)))
# print("Cleaned features:", cleaned)


feature_count = dict()

for phrase in cleaned:
    count = 0
    for word in phrase.split():
        if word not in stopwords_list:
            count += comments.words.count(word)
    feature_count[phrase] = count
    # print(phrase + ": " + str(count))

# counts = list(feature_count.values())
counts = feature_count.values()
# features = list(feature_count.keys())
features = feature_count.keys()
threshold = len(comments.noun_phrases) / 30  # 150 TODO
# threshold=66

print("Threshold:" + str(threshold))

frequent_features = []

for feature, count in feature_count.items():
    if count >= threshold and count >= 150: # 150 TODO
        frequent_features.append(feature)
print(' Features:', frequent_features[0:5])


def nltk_sentiment(sentence):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    nltk_sentiment = SentimentIntensityAnalyzer()
    score = nltk_sentiment.polarity_scores(sentence)
    return score


# b=dataset.values.T.tolist()
# print(b)
nltk_results = [nltk_sentiment(row) for row in frequent_features]
# print(nltk_results)
results_df = pd.DataFrame(nltk_results)
# print(nltk_results)

text_df = pd.DataFrame(frequent_features)
# print(text_df)
nltk_df = text_df.join(results_df)
# print(nltk_df.head(15))


newdf = pd.DataFrame({'features': nltk_df[0], 'pos': nltk_df['pos'], 'neg': nltk_df['neg']})
for index, row in newdf.iterrows():
    if row['features'] in feature_count:
        newdf.at[index, 'count'] = feature_count[row['features']]
    else:
        newdf.at[index, 'count'] = None
newdf.pos = newdf.pos + 0.2
newdf.neg = newdf.neg - 0.2
print(newdf)
with open('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/german_features.csv', 'w+', newline='',
          encoding='utf-8-sig') as file:
    newdf.to_csv(file, sep=',', na_rep='', float_format=None,
                 columns=['features', 'pos', 'neg', 'count'],
                 header=True, index=False, index_label=None, mode='a', compression='infer',
                 quoting=None, quotechar='"', line_terminator=None, chunksize=None,
                 doublequote=True, escapechar=None, decimal='.', errors='strict')
    file.close()

# pos = newdf[0:5]['pos']
# neg = newdf[0:5]['neg']

# data to plot
n_groups = 5
positive = newdf['pos'].head(5)
negative = newdf['neg'].head(5)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.2
opacity = 1

rects1 = plt.bar(index, positive, bar_width,
                 alpha=opacity,
                 color='b',
                 label='positive sentiments')

rects2 = plt.bar(index + bar_width, negative, bar_width,
                 alpha=opacity,
                 color='r',
                 label='negative sentiments')

plt.xlabel('Features')
plt.ylabel('sentiment value')
plt.title('Top features and its sentiment')
plt.xticks(index + bar_width, newdf['features'].head(5))
plt.legend()
fig.set_size_inches(10, 7.5)
plt.show()

absa_list = dict()
# For each frequent feature
# for comment in comments.split():
# blob = TextBlob(comments)
# For each sentence of the comment
for sentence in comments.sentences:
    # Search for frequent feature 'f'
    for f in frequent_features:
        # For each comment
        absa_list[f] = []
        q = '|'.join(f.split())
        if re.search(r'\w*(' + str(q) + ')\w*', str(sentence)):
            absa_list[f].append(sentence)

with open ('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/2020-02/german_aspect.txt', 'w+', encoding = 'utf-8-sig') as myfile:
    myfile.write(str(absa_list))
    myfile.close()
