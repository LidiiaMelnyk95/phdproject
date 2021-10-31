import pandas as pd

df = pd.read_excel('/Users/lidiiamelnyk/Downloads/youtube comments.xlsx', sheet_name= None)

data = pd.DataFrame() # Create an empty dataframe, this will be your final dataframe

for key, sub_df in df.items():
    data = data.append(sub_df, ignore_index=False) # Add your sub_df one by one
data['Reply'] = data['Reply'].astype(str)
#data['Comment'] = data['Comment'].astype(str)

for i,row in data.iterrows():
    for m in row['Reply'].split('\n'):
      data['Comment'].fillna(m)
data['Comment'].drop_duplicates()
data.dropna(subset = ['Comment'], inplace = True)
with open('/Users/lidiiamelnyk/Documents/youtube_comments.csv', 'w+', encoding='utf-8-sig', newline='') as my_file:
	data.to_csv(my_file, sep=',', na_rep='', float_format=None,
			   header=True, index=False, index_label=None,
			   mode='a', compression='infer',
			   quoting=None, quotechar='"', line_terminator=None, chunksize=None,
			   date_format=None, doublequote=True, escapechar=None, decimal='.')