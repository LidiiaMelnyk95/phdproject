import pandas as pd


data = pd.read_csv('/Users/lidiiamelnyk/Documents/youtube_comments.csv', sep = ';')


import emoji
def emoji_to_text(text):
    return (emoji.demojize(text, language = 'de'))

import re

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

for i,row in data.iterrows():
    for k in row['Comment'].split('\n' ):
        deemojized = remove_tags(emoji_to_text(k))
        data.at[i, 'Comment'] = deemojized

print(data['Comment'].head(10))
with open('/Users/lidiiamelnyk/Documents/youtube_comments.csv', 'w+', encoding='utf-8-sig', newline='') as my_file:
	data.to_csv(my_file, sep=',', na_rep='', float_format=None,
			   header=True, index=False, index_label=None,
			   mode='a', compression='infer',
			   quoting=None, quotechar='"', line_terminator=None, chunksize=None,
			   date_format=None, doublequote=True, escapechar=None, decimal='.')