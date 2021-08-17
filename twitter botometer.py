import botometer
import pandas as pd
import glob
import os

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
for i, row in df.iterrows():
    blt_scores = []
    for k in row['user.screen_name'].split(' '):  # .split('\n'):
        blt_score1 = blt_twitter.check_account(k)
        blt_score = round(blt_score1['cap']['universal'], 2)
        blt_scores.append(blt_score)
# print(blt_scores)
    df.at[i, 'bot_score'] =blt_scores

print(df.quantile(q=0.95, axis=df['Bot_score'], numeric_only=True, interpolation='linear'))
