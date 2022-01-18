import time

import botometer
import pandas as pd
import glob
import os
import tweepy
import requests

rapidapi_key = "1b47c699f8mshc1e15b6f0dc3ab7p1d8f63jsna0ae42e3ac74"
twitter_app_auth = {
    'consumer_key': 'DQ57uAy2pJ0JyyHvHHV156iVE',
    'consumer_secret': 'IMbybOm94Bmg4IychoFkCzu9qWvB7kmFMkPfzfzhiIGnxp7nSY',
    'access_token': '1333491145717010432-800PLQvPa4K378KNXXwiVrV1S8bJCC',
    'access_token_secret': 'd9AjCyke83sRgzw2X3kXGoQBWiLjgKKXbmrpqWIJAHC3L'
}
all_files = glob.glob('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/2020-02/german/*.csv')
blt_twitter = botometer.Botometer(consumer_key=twitter_app_auth['consumer_key'],
                                  consumer_secret=twitter_app_auth['consumer_secret'],
                                  access_token=twitter_app_auth['access_token'],
                                  access_token_secret=twitter_app_auth['access_token_secret'],
                                  rapidapi_key=rapidapi_key)
#df = pd.concat(map(pd.read_csv,
 #                  glob.glob(os.path.join('/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/2020-01/', "*.csv"))))

blt_scores = []

for filename in all_files:
    df = pd.read_csv(filename, sep = ';', header = 0)
    print(filename)
    for i, row in df.iterrows():
        df['user.screen_name'] = df['user.screen_name'].astype(str)
        try:
            for k in row['user.screen_name'].split(' '):  # .split('\n'):
                blt_score1 = blt_twitter.check_account(k)
                time.sleep(3)
                blt_score = round(blt_score1['cap']['universal'], 2)
                df.at[i, 'bot_score'] = blt_score
                print(blt_score)
        except tweepy.error.TweepError or AttributeError or ReadTimeoutError:
            continue
        df = df.reindex(columns=['full_text', 'user.screen_name', 'created_at', 'bot_score', 'entities.hashtags',
                             'entities.symbols', 'entities.user_mentions', 'entities.urls', 'entities.media'])
    with open(filename, 'w+', newline='',encoding='utf-8-sig') as file:
        df.to_csv(file, sep=',', na_rep='', float_format=None,
                columns=['full_text', 'user.screen_name', 'created_at', 'bot_score', 'entities.hashtags',
                        'entities.symbols', 'entities.user_mentions', 'entities.urls', 'entities.media'],
                header=True, index=False, index_label=None, mode='a', compression='infer',
                quoting=None, quotechar='"', line_terminator=None, chunksize=None,
                doublequote=True, escapechar=None, decimal='.', errors='strict')
        file.close()
    print('finished')




    file.close()