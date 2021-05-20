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

file = pd.read_csv('/Users/lidiiamelnyk/Documents/lemmatized_dataframe.csv',  sep = ',', encoding='utf-8-sig',
                         float_precision='round_trip')

#sent = file['lemmatized'].astype(str)
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

word_freq = defaultdict(int)
for sent in sentences:
    for i in sent:
        word_freq[i] += 1 #basically calculate each new word
print(len(word_freq))

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
from nltk.cluster import KMeansClusterer
import nltk

from sklearn import cluster
from sklearn import metrics

NUM_CLUSTERS = 5
kmeans = cluster.KMeans(n_clusters=NUM_CLUSTERS)
kmeans.fit(X)

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

import time

import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.datasets import make_blobs

# #############################################################################
# Generate sample data
np.random.seed(0)

batch_size = 45
centers = [[1, 1], [-1, -1], [1, -1]]
n_clusters = len(centers)
X, labels_true = make_blobs(n_samples=3000, centers=centers, cluster_std=0.7)

# #############################################################################
# Compute clustering with Means

k_means = KMeans(init='k-means++', n_clusters=3, n_init=10)
t0 = time.time()
k_means.fit(X)
t_batch = time.time() - t0

# #############################################################################
# Compute clustering with MiniBatchKMeans

mbk = MiniBatchKMeans(init='k-means++', n_clusters=3, batch_size=batch_size,
                      n_init=10, max_no_improvement=10, verbose=0)
t0 = time.time()
mbk.fit(X)
t_mini_batch = time.time() - t0

# #############################################################################
# Plot result

fig = plt.figure(figsize=(8, 3))
fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
colors = ['#4EACC5', '#FF9C34', '#4E9A06']

# We want to have the same colors for the same cluster from the
# MiniBatchKMeans and the KMeans algorithm. Let's pair the cluster centers per
# closest one.
k_means_cluster_centers = k_means.cluster_centers_
order = pairwise_distances_argmin(k_means.cluster_centers_,
                                  mbk.cluster_centers_)
mbk_means_cluster_centers = mbk.cluster_centers_[order]

k_means_labels = pairwise_distances_argmin(X, k_means_cluster_centers)
mbk_means_labels = pairwise_distances_argmin(X, mbk_means_cluster_centers)

# KMeans
ax = fig.add_subplot(1, 3, 1)
for k, col in zip(range(centroids), colors):
    my_members = k_means_labels == k
    cluster_center = k_means_cluster_centers[k]
    ax.plot(X[my_members, 0], X[my_members, 1], 'w',
            markerfacecolor=col, marker='.')
    ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=6)
ax.set_title('KMeans')
ax.set_xticks(())
ax.set_yticks(())
plt.text(-3.5, 1.8,  'train time: %.2fs\ninertia: %f' % (
    t_batch, k_means.inertia_))