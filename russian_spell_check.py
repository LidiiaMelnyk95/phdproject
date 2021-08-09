import pandas as pd
from symspellpy import SymSpell, Verbosity

dataframe1 = pd.read_csv("/Users/lidiiamelnyk/Documents/korrespondent/all_comments_edited.csv", sep=',',
                         encoding='utf-8-sig',
                         float_precision='round_trip')

russian_dataframe = dataframe1[dataframe1['predicted_language'] == 'Russian']
#russian_dataframe = russian_dataframe.drop_duplicates()
sym_spell = SymSpell()

corpus_path = "/Users/lidiiamelnyk/Downloads/dss-plugin-nlp-preparation-main/resource/dictionaries/ru.txt"
symspell_dictionary = sym_spell.load_dictionary(corpus_path, term_index=0, count_index=1, separator=None,
                                                encoding='utf-8-sig')

russian_dataframe['edited'] = russian_dataframe['edited'].astype(str)
russian_dataframe['comments_corrected'] = russian_dataframe['edited'].apply(lambda x:
                                                                             (sym_spell.lookup(x, Verbosity.CLOSEST, max_edit_distance=0, include_unknown = True,  transfer_casing=False,ignore_token=r"\w+\d")))

print(russian_dataframe['edited'].count())
for i, row in russian_dataframe.iterrows():
    if len(row['comments_corrected']) > 0:
        pass
    else:
        row['edited'].replace(to_replace=[i for i in row['comment']], value=[i for i in row['comments_corrected']], inplace=False, limit=None,
                                regex=False, method='pad')

   # print(ukrainian_dataframe['comment'].head())
print(russian_dataframe['edited'].count())

print(russian_dataframe['edited'].head())
with open('/Users/lidiiamelnyk/Documents/korrespondent/all_comments_ru_corrected.csv', 'w+', newline = '', encoding='utf-8-sig') as file:
    russian_dataframe.to_csv(file, sep=',', na_rep='', float_format=None,
               columns=['url', 'edited', 'date', 'name','predicted_language'],
               header=True, index=False, index_label=None,
               mode='a', compression='infer',
               quoting=None, quotechar='"', line_terminator=None, chunksize=None,
               date_format=str, doublequote=True, escapechar=None, decimal='.', errors='strict')
    file.close()