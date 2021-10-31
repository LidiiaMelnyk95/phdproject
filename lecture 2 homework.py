import numpy as np
import matplotlib.pyplot as plt
import sklearn

import pandas as pd
data = pd.read_csv("/Users/lidiiamelnyk/nlp_course/week02_classification/comments.tsv", sep='\t', encoding = 'utf-8-sig')
data.dropna(subset = ['comment_text', 'should_ban'], inplace = True)

texts = data['comment_text']
texts = pd.array(texts, dtype="string")
#texts = np.array2string(texts)
target = data['should_ban']
from sklearn.model_selection import train_test_split


texts_train, texts_test, y_train, y_test = train_test_split(texts, target, test_size=0.5, random_state=42)


from nltk.tokenize import TweetTokenizer
tokenizer = TweetTokenizer( )
texts_train = [t.lower() for t in texts_train]
texts_test = [t.lower() for t in texts_test]
texts_train_2 = []
texts_test_2 = []
preprocess = lambda text: ' '.join(tokenizer.tokenize(text))
for i in texts_train:
    preprocess_line = preprocess(i)
    texts_train_2.append(preprocess_line)
for i in texts_test:
    preprocess_test = preprocess(i)
    texts_test_2.append(preprocess_test)



assert texts_train_2[5] == 'who cares anymore . they attack with impunity .'
assert texts_test_2[89] == 'hey todds ! quick q ? why are you so gay'
assert len(texts_test) == len(y_test)

import collections
k = 1000
c = collections.Counter()

for sentence in texts_train_2: #for each line in a list of strings
    for word in tokenizer.tokenize(sentence): #for each word in a line
        c[word] += 1 # if word in a line, count as one

bow_vocabulary = list([i[0] for i in c.most_common(k)]) #create a list of words (not values) in the most common words
print('example features:', sorted(bow_vocabulary)[::500])


def text_to_bow(text) -> np.array:
    """ convert text string to an array of token counts. Use bow_vocabulary. """
    bow = bow_vocabulary #use vocabulary
    tmp = [] #create an empty list
    for ch_bow in bow: #for an element in a vocabulary
        val = 0
        for ttk in tokenizer.tokenize(text): #for element in text
            if ch_bow == ttk: #if element from a vocabulary in text
                val += 1 #calculate its number
        tmp.append(val) #create the list of frequencies

    return np.array(tmp, 'float32')

X_train_bow = np.stack(list(map(text_to_bow, texts_train_2)))
X_test_bow = np.stack(list(map(text_to_bow, texts_test_2)))




k = 1000

k_max = len(set(' '.join(texts_train_2).split())) #maximal lengths of k is the length of unique words in texts_train_2
assert X_train_bow.shape == (len(texts_train_2), min(k, k_max))
assert X_test_bow.shape == (len(texts_test), min(k, k_max))

class BinaryNaiveBayes:
    delta = 1.0
    