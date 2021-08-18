import time

import botometer
import pandas as pd
import glob
import os

import requests

rapidapi_key = "1b47c699f8mshc1e15b6f0dc3ab7p1d8f63jsna0ae42e3ac74"
twitter_app_auth = {
    'consumer_key': 'DQ57uAy2pJ0JyyHvHHV156iVE',
    'consumer_secret': 'IMbybOm94Bmg4IychoFkCzu9qWvB7kmFMkPfzfzhiIGnxp7nSY',
    'access_token': '1333491145717010432-800PLQvPa4K378KNXXwiVrV1S8bJCC',
    'access_token_secret': 'd9AjCyke83sRgzw2X3kXGoQBWiLjgKKXbmrpqWIJAHC3L'
}

blt_twitter = botometer.Botometer(consumer_key=twitter_app_auth['consumer_key'],
                                  consumer_secret=twitter_app_auth['consumer_secret'],
                                  access_token=twitter_app_auth['access_token'],
                                  access_token_secret=twitter_app_auth['access_token_secret'],
                                  rapidapi_key=rapidapi_key)
df = pd.concat(map(pd.read_csv,
                   glob.glob(os.path.join('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/2020-01/', "*.csv"))))
df['user.screen_name'] = df['user.screen_name'].astype(str)
blt_scores = []
df = df.reindex(columns = ['full_text', 'user.screen_name','created_at', 'bot_score', 'entities.hashtags',	'entities.symbols',	'entities.user_mentions',	'entities.urls',	'entities.media'])
for i, row in df.iterrows():
    for k in row['user.screen_name'].split(' '):  # .split('\n'):
        try:
            blt_score1 = blt_twitter.check_account(k)
            time.sleep(30)
            blt_score = round(blt_score1['cap']['universal'], 2)
            blt_scores.append(blt_score)
            df.at[i,'bot_score'] = blt_score
            with open('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/botometer_added.csv', 'w+', newline='',
                      encoding='utf-8-sig') as file:
                df.to_csv(file, sep=',', na_rep='', float_format=None,
                          columns=['full_text', 'user.screen_name', 'created_at', 'bot_score', 'entities.hashtags',
                                   'entities.symbols', 'entities.user_mentions', 'entities.urls', 'entities.media'],
                          header=True, index=False, index_label=None,
                          mode='a', compression='infer',
                          quoting=None, quotechar='"', line_terminator=None, chunksize=None,
                          doublequote=True, escapechar=None, decimal='.', errors='strict')
        except requests.exceptions.HTTPError:
            continue
        print(blt_scores)




    file.close()