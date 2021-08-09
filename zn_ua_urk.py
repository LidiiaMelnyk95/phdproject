import fasttext

fasttext.FastText.eprint = lambda x: None
import pandas as pd
model = fasttext.load_model("model1.bin")

data_in = pd.read_csv('/Users/lidiiamelnyk/Documents/korrespondent/all_comments_ukr_corrected.csv')

all_rows = 0
hate_rows = 0
for i, row in data_in.iterrows():
    try:
        current_data = row['comment'].replace('\n', ' ')
        model_result = model.predict(str(current_data))

        if model_result[0][0] == '__label__HATE':
            #print(current_data)
            hate_rows = hate_rows + 1
        data_in.at[i, 'model_result'] = model_result[0][0]

    except:
        continue
all_rows = len(data_in.index)
if all_rows > 0 :
    percent = (hate_rows / all_rows) * 100

print("\tMonth :  \n All rows per month {} hate rows per month {} percentage {:.2f} %".format( all_rows, hate_rows, percent))
with open('/Users/lidiiamelnyk/Documents/korrespondent/hatespeech_censor_ua.csv', 'w+', newline='', encoding='utf-8-sig') as myfile:
    data_in.to_csv(myfile, sep=',', na_rep='', float_format=None,
               header=True, index=True, index_label=None,
               mode='w', compression='infer',
               quoting=None, quotechar='"', line_terminator=None, chunksize=None,
               date_format= str, doublequote=True, escapechar=None, decimal='.', errors='strict')
    myfile.close()