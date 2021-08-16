import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
import glob
import os
import stanza
stanza.download('uk')



config = {
	'processors': 'tokenize,mwt,pos', # Comma-separated list of processors to use
	'lang': 'fr', # Language code for the language to build the Pipeline in
	'tokenize_model_path': './fr_gsd_models/fr_gsd_tokenizer.pt', # Processor-specific arguments are set with keys "{processor_name}_{argument_name}"
	'mwt_model_path': './fr_gsd_models/fr_gsd_mwt_expander.pt',
	'pos_model_path': './fr_gsd_models/fr_gsd_tagger.pt',
	'pos_pretrain_path': './fr_gsd_models/fr_gsd.pretrain.pt',
	'tokenize_pretokenized': True # Use pretokenized text as input and disable tokenization
}

nlp = stanza.Pipeline('uk', processors='tokenize, pos, lemma', tokenize_no_ssplit = True) #create nlp pipeline
myfile = open('/Users/lidiiamelnyk/Documents/stop_words_ua.txt', "r", encoding = 'utf-8-sig') #upload the stopwords
content = myfile.read()
stopwords_list = content.split("\n") #since stopwords come in a form of a list, split them based on the newline
df = pd.concat(map(pd.read_csv, glob.glob(os.path.join('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/2020-01/', "*.csv"))))

for iter, row in df.iterrows():
	lemmatized_sents = [] #create the list, I am going to append lemmas into
	df['full_text'] = df['full_text'].astype(str) #change type of data to str as it is required to process the file in the nlp pipeline
	if isinstance(row['full_text'],float): #handling the failure where it is for some reason always tpe float
		continue
	doc = nlp(row['full_text']) #create the doc file from the nlp pipeline
	try:
		sentenciz = doc.sentences[0].tokens #get tokens
		for t in sentenciz:
			pos_tags = t.words[0].pos #for each token get the part of speech tag
			allowed_tags = ['VERB', 'NOUN', 'PROPN', 'ADJ', 'DET', 'ADV', 'NUM'] #create the list of tags I want to sort by
			for tag in pos_tags.split(' '):
				if tag in allowed_tags:
					lemmas = t.words[0].lemma.lower()
					for lemma in lemmas.split():
						if lemma not in stopwords_list:
							lemmatized_sents.append(lemmas)
		df.at[iter, 'lemmatized'] = ','.join(lemmatized_sents)
	except IndexError:
		pass


items = set()

new_df = df["lemmatized"].str.split(",", expand = True)
for col in new_df:
    items.update(new_df[col].unique())


print(items)
#custom one hot encoding
itemset = set(items)
encoded_vals = []
for index, row in new_df.iterrows():
	rowset = set(row)
	labels = {}
	uncommons = list(itemset - rowset)
	commons = list(itemset.intersection(rowset))
	for uc in uncommons:
		labels[uc] = 0
	for com in commons:
		labels[com] = 1
	encoded_vals.append(labels)
encoded_vals[0]

ohe_df = pd.DataFrame(encoded_vals)


