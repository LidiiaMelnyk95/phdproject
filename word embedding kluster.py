import pandas as pd
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
from gensim.models.phrases import Phrases, Phraser
import numpy as np
import itertools
from time import time  # To time our operations
from collections import defaultdict  # For word frequency
import multiprocessing
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree
import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)

f = pd.read_csv('/Users/lidiiamelnyk/Documents/korrespondent/processed/lemmatized_dataframe_ru.csv',  sep = ',', encoding='utf-8-sig',
                         float_precision='round_trip')
file = f[f['model_result']=='__label____label__HATE']
#sent = file['lemmatized'].astype(str)
import re
for i, row in file.iterrows():
    sent = []
    file['lemmatized'] = file['lemmatized'].astype(str)
    try:
        if isinstance(row['lemmatized'], float):  # handling the failure where it is for some reason always tpe float
            continue
        for word in row['lemmatized'].split(' '):
            words = re.findall('\w+', word)
            words = " ".join(words)
            sent.append(words)
        file.at[i, 'edited'] =" ,".join(sent)
    except KeyError:
        print('keyerror')
        pass

sent1 = [row.split() for row in file['edited'].astype(str)]

#phrases = Phrases(sent1, min_count=1, progress_per=10000)

#bigram = Phraser(phrases)

#sentences = bigram[sent1]
#carry out the word frequency calculations as a sanity check of the effectiveness of the lemmatization, removal of stopwords, and addition of bigrams.



#3 steps of building the model: In this first step, I set up the parameters of the model one-by-one.
# Here it builds the vocabulary from a sequence of sentences and thus initialized the model.
#train the model
feature_size = 50
cores = multiprocessing.cpu_count() # Count the number of cores in a computer
w2v_model = Word2Vec(min_count= 3, #the words (bigrams) should be met in a corpus at least this number of times
                     window= 6,  #The maximum distance between the current and predicted word within a sentence. E.g. window words on the left and window words on the left of our target
                     sample= 2e-5, #float - The threshold for configuring which higher-frequency words are randomly downsampled. Highly influencial.
                     alpha=1.1, #The initial learning rate
                     min_alpha=0.0078, # Learning rate will linearly drop to min_alpha as training progresses.
                     negative= 9, #negative sampling will be used, the int for negative specifies how many "noise words" should be drown.
                     workers=cores-1) #Use these many worker threads to train the model (=faster training with multicore machines


w2v_model.build_vocab(sent1, progress_per=100)

t = time()


print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))

w2v_model.train(sent1, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1) #total examples is count of sentences, epochs is number of iterations over a corpus

print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))

X = w2v_model.wv.vectors
words = w2v_model.wv.index_to_key
from nltk.cluster import KMeansClusterer
import nltk

from sklearn import cluster
from sklearn import metrics

NUM_CLUSTERS = 5
kmeans = cluster.KMeans(n_clusters=NUM_CLUSTERS)
kmeans.fit(X)
import matplotlib.pyplot as plt


labels = kmeans.labels_
centroids = kmeans.cluster_centers_

print("Cluster id labels for inputted data")
print(labels)

print(
    "Score (Opposite of the value of X on the K-means objective which is Sum of distances of samples to their closest cluster center):")
print(kmeans.score(X))

silhouette_score = metrics.silhouette_score(X, labels, metric='euclidean')

print("Silhouette_score: ")
print(silhouette_score)

for i, word in enumerate(words):
    print(word + ":" + str(labels[i]))

plt.scatter(X[:, 0], X[:, 1], c=labels,
            s=50, cmap='viridis')


plt.show()

from sklearn.metrics import pairwise_distances_argmin


def find_clusters(X, n_clusters, rseed=4):
    # 1. Randomly choose clusters
    rng = np.random.RandomState(rseed)
    i = rng.permutation(X.shape[0])[:n_clusters]
    centers = X[i]

    while True:
        # 2a. Assign labels based on closest center
        labels = pairwise_distances_argmin(X, centers)

        # 2b. Find new centers from means of points
        new_centers = np.array([X[labels == i].mean(0)
                                for i in range(n_clusters)])

        # 2c. Check for convergence
        if np.all(centers == new_centers):
            break
        centers = new_centers

    return centers, labels


centers, labels = find_clusters(X, 5)

plt.scatter(X[:, 0], X[:, 1], c=labels,
            s=50, cmap='viridis')


plt.show()
