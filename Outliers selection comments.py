import pandas as pd
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser
from time import time  # To time our operations
from collections import defaultdict, Counter  # For word frequency
import multiprocessing
import logging  # Setting up the loggings to monitor gensim
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)

file = pd.read_csv('/Users/lidiiamelnyk/Documents/lemmatized_dataframe.csv',  sep = ',', encoding='utf-8-sig',
                         float_precision='round_trip')
aggregate_counter = Counter()
for i, row in file.iterrows():
    file['lemmatized'] = file['lemmatized'].astype(str)
    c = Counter(row['lemmatized'].split())
    aggregate_counter += c

common_words = [word[0] for word in aggregate_counter.most_common(50)]
common_words_counts =  [word[1] for word in aggregate_counter.most_common(50)]

def barplot(words, word_count, title):
    fig = plt.figure(figsize = (18,6))
    bar_plot = sns.barplot(x = words, y = word_count)
    for item in bar_plot.get_xticklabels():
        item.set_rotation(90)
    plt.title(title)
    plt.show()

barplot(words=common_words, word_count=common_words_counts, title='Most Frequent Words used in the comments')


from itertools import islice

def key_word_counter(tupple):
    return tupple[1]

all_word_counts = sorted(aggregate_counter.items(), key=key_word_counter)
uncommon_words = [word[0] for word in islice(all_word_counts, 50)]
uncommon_word_counts = [word[1] for word in islice(all_word_counts, 50)]

barplot(words=uncommon_words, word_count=uncommon_word_counts, title='Least Frequent Words used in the comments')

import re
for iter, row in file.iterrows():
    sent = []
    file['lemmatized'] = file['lemmatized'].astype(str)
    if isinstance(row['lemmatized'], float):  # handling the failure where it is for some reason always tpe float
        continue
    for word in row['lemmatized'].split(' '):
        words = re.findall('\w+', word)
        words = " ".join(words)
        sent.append(words)
    file.at[iter, 'changed'] =" ,".join(sent)


sent1 =  [row.split() for row in file['changed'].astype(str)]

phrases = Phrases(sent1, min_count=20, progress_per=10000)

bigram = Phraser(phrases)

sentences = bigram[sent1]
#carry out the word frequency calculations as a sanity check of the effectiveness of the lemmatization, removal of stopwords, and addition of bigrams.

#3 steps of building the model: In this first step, I set up the parameters of the model one-by-one.
# Here it builds the vocabulary from a sequence of sentences and thus initialized the model.
#train the model
feature_size = 10
cores = multiprocessing.cpu_count() # Count the number of cores in a computer
w2v_model = Word2Vec(min_count=20, #the words (bigrams) should be met in a corpus at least this number of times
                     window=3,  #The maximum distance between the current and predicted word within a sentence. E.g. window words on the left and window words on the left of our target
                     sample=6e-5, #float - The threshold for configuring which higher-frequency words are randomly downsampled. Highly influencial.
                     alpha=0.07, #The initial learning rate
                     min_alpha=0.0007, # Learning rate will linearly drop to min_alpha as training progresses.
                     negative=15, #negative sampling will be used, the int for negative specifies how many "noise words" should be drown.
                     workers=cores-1) #Use these many worker threads to train the model (=faster training with multicore machines
t = time()

w2v_model.build_vocab(sentences, progress_per=10000)

print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))

w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=50, report_delay=1) #total examples is count of sentences, epochs is number of iterations over a corpus

print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))

X = w2v_model.wv.vectors
words = w2v_model.wv.index_to_key

from sklearn.neural_network import MLPRegressor
auto_encoder = MLPRegressor(hidden_layer_sizes=(
                                                 600,
                                                 150,
                                                 600,
                                               ))
auto_encoder.fit(X, X) #features will be compared and contrasted against each other
predicted_vectors = auto_encoder.predict(X)
print(predicted_vectors) #predicted vestors are output vectors

print(auto_encoder.score(predicted_vectors, X)) #check the accuracy of the Regression
pd.DataFrame(auto_encoder.loss_curve_).plot()
plt.show()

