from typing import List, Any, Union

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mosestokenizer import *
import re
# Alternative manual download link: https://yadi.sk/d/_nGyU2IajjR9-w
data = pd.read_json("/Users/lidiiamelnyk/Downloads/arxivData.json")
data.sample(n=5)
# assemble lines: concatenate title and description
lines = data.apply(lambda row: row['title'] + ' ; ' + row['summary'], axis = 1).tolist()
print(sorted(lines, key=len)[:3])

tokenizer = MosesTokenizer('en')
lines_tokenized: list[list[Union[list[Any], list[str]]]] = []
for line in lines:
    line_list = []
    for i in line.split('.'):
        entities = i.lower().replace('\n', ' ')
        for k in entities.split(' '):
            token = tokenizer(k)
            line_list.append(token)
    line_list = str(line_list).replace('[', '').replace(']', '').replace("'", '').replace(',', ' ')
    lines_tokenized.append(line_list)


from tqdm import tqdm
from collections import defaultdict, Counter, deque

UNK, EOS = "_UNK_", "_EOS_"

counts = defaultdict(Counter)
def count_ngrams(lines_tokenized, n):
    for line in lines_tokenized:
        tokens = line.split()
        tokens.append (EOS)
        prefix = deque([UNK] * (n-1), maxlen = n - 1)
        for tok in tokens:
            counts[tuple(prefix)][tok] += 1
            prefix.append(tok)

    return counts

dummy_lines = sorted(lines_tokenized, key = len)[:100]
dummy_counts = count_ngrams(dummy_lines, n=3)
assert set(map(len, dummy_counts.keys())) == {2}, "please only count {n-1}-grams"
assert dummy_counts['_UNK_', 'a']['note'] == 2
assert dummy_counts['p', '=']['np'] == 2

class NgramLanguageModel:

    def __init__(self, lines_tokenized, n):
        assert n>1
        self.n = n

        counts = count_ngrams(lines_tokenized, n)
        # compute token proabilities given counts
        self.probs = defaultdict(Counter)
        for words in counts.keys():
            for word in counts[words].keys():
                self.probs[words][word] = counts[words][word]/sum(counts[words].values())


    def get_possible_next_tokens(self, prefix):
        """
        :param prefix: string with space-separated prefix tokens
        :returns: a dictionary {token : it's probability} for all tokens with positive probabilities
        """
        prefix = prefix.split()
        prefix = prefix[max(0, len(prefix) - self.n + 1):]
        prefix = [UNK] * (self.n - 1 - len(prefix)) + prefix
        return self.probs[tuple(prefix)]


    def get_next_token_prob(self, prefix, next_token):
        """
        :param prefix: string with space-separated prefix tokens
        :param next_token: the next token to predict probability for
        :returns: P(next_token|prefix) a single number, 0 <= P <= 1
        """
        return self.get_possible_next_tokens(prefix).get(next_token, 0)
