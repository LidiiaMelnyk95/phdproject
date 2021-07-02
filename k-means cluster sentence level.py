from gensim.models import Word2Vec

from nltk.cluster import KMeansClusterer
import nltk
import numpy as np

from sklearn import cluster
from sklearn import metrics

# training data

import pandas as pd
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser
from time import time  # To time our operations
from collections import defaultdict  # For word frequency
import multiprocessing
import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)

f = pd.read_csv('/Users/lidiiamelnyk/Documents/lemmatized_dataframe.csv',  sep = ',', encoding='utf-8-sig',
                         float_precision='round_trip')
file = f[f['model_result']=='__label____label__HATE']

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


sentences =  [row.split() for row in file['changed'].astype(str)]

#carry out the word frequency calculations as a sanity check of the effectiveness of the lemmatization, removal of stopwords, and addition of bigrams.

word_freq = defaultdict(int)


#3 steps of building the model: In this first step, I set up the parameters of the model one-by-one.
# Here it builds the vocabulary from a sequence of sentences and thus initialized the model.
#train the model
feature_size = 10
cores = multiprocessing.cpu_count() # Count the number of cores in a computer
w2v_model = Word2Vec(min_count=10, #the words (bigrams) should be met in a corpus at least this number of times
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

model = Word2Vec(sentences, min_count=1)


def sent_vectorizer(sent, model):
    sent_vec = []
    numw = 0
    for w in sent:
        try:
            if numw == 0:
                sent_vec = model[w]
            else:
                sent_vec = np.add(sent_vec, model[w])
            numw += 1
        except:
            pass

    return np.asarray(sent_vec) / numw


model_vectors = []
for sentence in sentences:
    model_vectors.append(sent_vectorizer(sentence, model))

print("========================")
print(X)



NUM_CLUSTERS = 2
kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=15, avoid_empty_clusters = True)
assigned_clusters = kclusterer.cluster(model_vectors, assign_clusters=True)
print(assigned_clusters)

for index, sentence in enumerate(sentences):
    print(str(assigned_clusters[index]) + ":" + str(sentence))

kmeans = cluster.KMeans(n_clusters=NUM_CLUSTERS)
kmeans.fit(X)

labels = kmeans.labels_
centroids = kmeans.cluster_centers_

print("Cluster id labels for inputted data")
print(labels)
print("Centroids data")
print(centroids)

print(
    "Score (Opposite of the value of X on the K-means objective which is Sum of distances of samples to their closest cluster center):")
print(kmeans.score(X))

silhouette_score = metrics.silhouette_score(X, labels, metric='euclidean')

print("Silhouette_score: ")
print(silhouette_score)

import matplotlib.pyplot as plt

from sklearn.manifold import TSNE

model = TSNE(n_components=2, random_state=0)
np.set_printoptions(suppress=True)

Y = model.fit_transform(X)

plt.scatter(Y[:, 0], Y[:, 1], c=assigned_clusters, s=290, alpha=.5)

for j in range(len(sentences)):
    plt.annotate(assigned_clusters[j], xy=(Y[j][0], Y[j][1]), xytext=(0, 0), textcoords='offset points')
    print("%s %s" % (assigned_clusters[j], sentences[j]))

plt.show()