from germansentiment import SentimentModel

model = SentimentModel()
import pandas as pd
texts = [
    "Mit keinem guten Ergebniss", "Das ist gar nicht mal so gut",
    "Total awesome!", "nicht so schlecht wie erwartet",
    "Der Test verlief positiv.", "Sie fährt ein grünes Auto."]
data = pd.read_csv('/Users/lidiiamelnyk/Documents/youtube_comments_1001_2000.csv', sep = ';',error_bad_lines=False)
list_text=[] #your empty list

for i, row in data.iterrows():
    list_row = []
    for k in row['Comment'].split('/n'):
        for l in k.split('.'):
            list_row.append(l)
        list_text.append(list_row)

result_list = []
for l in list_text:
    result = model.predict_sentiment(l)
    result_list.append(result)

data['Sentiment'] = result_list[:1000]

#new_columns = ['Name', 'Comment', 'Time', 'Sentiment']
#data = data.reindex(new_columns)
with open('/Users/lidiiamelnyk/Documents/youtube_comments_sentiment_1001_2000.csv', 'w+', encoding='utf-8-sig', newline='') as my_file:
    data.to_csv(my_file, sep=',', na_rep='', float_format=None,
			   header=True, index=False, index_label=None,
			   mode='a', compression='infer',
			   quoting=None, quotechar='"', line_terminator=None, chunksize=None,
			   date_format=None, doublequote=True, escapechar=None, decimal='.')
