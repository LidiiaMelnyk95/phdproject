import pandas as pd
import numpy as np
import glob
import gzip
import json

pd.set_option('display.max_columns', 500)

all_files = glob.glob('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/2020-02/*.jsonl.gz')

for filename in all_files:
    with gzip.open(filename, 'rt') as f:
        try:
            data = pd.DataFrame(f.read().splitlines(),columns = ['json'], index = None)
       # data = data['json'].apply(json.loads)
            f.close()
            df_final = pd.json_normalize(data['json'].apply(json.loads))
            filename1 = filename[:-9] + '.csv'
            try:
                df_ukrainian = df_final[df_final["lang"] == 'uk']
                with open(filename1, 'w+', encoding='utf-8-sig', newline='') as file:
                    df_ukrainian.to_csv(file, sep=',', na_rep='', float_format=None,
                            header=True, index=False, index_label=None,
                            mode='a', compression='infer',
                            quoting=None, quotechar='"', line_terminator=None, chunksize=None,
                            date_format=None, doublequote=True, escapechar=None, decimal='.')
                print("Finished writing to {}".format(filename1))
                file.close()
            except KeyError:
                continue
        except EOFError:
            continue



print(df_ukrainian.head())