import datetime

import tweepy
import json
import pandas as pd
import concurrent.futures
from tweepy import OAuthHandler

api_key = 'WF09qfCfgY0scJZWXxxm4Uit8'
api_secret = 'B6CrYljAf9OinLLlUo7cPibSxUBlHthesA6GeVCCiQMk0JhMoT'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAFiARQEAAAAApOzRPUZ1QACvv68TtG5GTZm2XLQ%3DUYcHcx78euvWf39fjJKpV4jEKEVRfGOf03twOGaSoVVVpy4XEb'

access_key = '1333491145717010432-eYn43gAohTYNoXyhqR8hvPO4eg1PRV'
access_secret = 'odnyMlaXRMpDohnUi4H3VrWRzcrz9LklCcTKwJ4ruUdhH'
auth = OAuthHandler(api_key, api_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

query_list = ['uefa rainbow','UEFA regenbogen', 'euro2020 rainbow', 'regenbogen', 'uefa human rights','Manuel neuer, kapitänsbinde',
              'Ungarn uefa', 'Allianz Arena Regenbogen','ungger regenbogen', 'hun-ger rainbox', 'gerhun regenbogen', 'Regenbogenfarben',
              'Regenbogenfahne Flitzer', 'Dfb_team','UEFA Homophobie', 'UEFA LGBTQ+', 'UEFA LGBT', 'EM2021 LGBT', 'EM2021 LGBTQ+', 'UEFA Anti-LGBTQ',
              'UEFA diskriminierend', 'Euro2021 homophobisch','regenbogenfanne', 'regenbogenverbot', 'regenbogenfanneverbot', 'regenbogen verbot',
              'Regenbogen-Stadion', 'Regenbogen-Stadion verbot', 'UEFA Verbot',
              'Regenbogen-Verbot', 'regenbogenbeleuchtung', 'UEFA politisch', 'Regenbogenbanden', 'UEFA Euro2020 Regenbogen', 'keine Regenbogenfarben EURO2020',
              'Kapitanverband Regenbogen', 'EM2020 LGBT']

#query_list = ['regenbogenfanne', 'regenbogenverbot', 'regenbogenfanneverbot', 'regenbogen verbot', 'Regenbogen-Stadion', 'Regenbogen-Stadion verbot', 'UEFA Verbot'
#              'Regenbogen-Verbot', 'regenbogenbeleuchtung', 'UEFA politisch', 'Regenbogenbanden']

#query_list = ['UEFA Homophobie', 'UEFA LGBTQ+', 'UEFA LGBT', 'EM2021 LGBT', 'EM2021 LGBTQ+', 'UEFA Anti-LGBTQ', 'UEFA diskriminierend', 'Euro2021 homophobisch']
tweets_list = []
from datetime import date
today_date = date.today()
time_delta = datetime.timedelta(days = 7)
time_delta_2 =  datetime.timedelta(days = 3)

def get_tweets(q):
    tweets = api.search(q, since = today_date - time_delta, until = today_date, tweet_mode = 'extended', count = 100, language = 'de')
    for tweet in tweets:
        text = tweet._json['full_text']
        user_name = tweet._json['user']['screen_name']
        user_id = tweet._json['user']['id']
        date = tweet._json['created_at']
        language = tweet._json['lang']
        tweet_id = tweet._json['id']
        tweet_geo = tweet._json['user']['location']
        tweets_list.append({'tweet_text': text, 'user_name': user_name, 'user_id': user_id, 'date': date, 'language': language, 'tweet_id': tweet_id,
                            'location': tweet_geo})
    return tweets_list

def get_data(q):
    tweet_text_array = []
    tweets = get_tweets(q)
    tweet_text_array = tweet_text_array + tweets
    rows = []
    columns_names = 'tweet_text', 'user_name', 'user_id', 'date', 'language', 'tweet_id', 'tweet_geo'
    df1 = pd.DataFrame(columns=columns_names)
    for item in tweet_text_array:
        rows.append({'tweet_text': item.get('tweet_text'), 'user_name': item.get('user_name'), 'user_id': item.get('user_id'),
                      'date': item.get('date'), 'language': item.get('language'), 'tweet_id': item.get('tweet_id'), 'tweet_geo': item.get('tweet_geo')})

    df1 = df1.append(rows, ignore_index=True)
    df1 = df1.drop_duplicates()
    filename = "/Users/lidiiamelnyk/Documents/tweets_uefa/" + q + '.csv'
    with open(filename, 'a', encoding='utf-8-sig', newline='') as file:
        df1.to_csv(file, sep=',', na_rep='', float_format=None,
                   columns=[ 'tweet_text', 'user_name', 'user_id', 'date', 'language', 'tweet_id'],
                   header=True, index=False, index_label=None,
                   mode='a', compression='infer',
                   quoting=None, quotechar='"', line_terminator=None, chunksize=None,
                   date_format=None, doublequote=True, escapechar=None, decimal='.')
    print("Finished writing to {}".format(filename))
    file.close()
    count = df1['tweet_text'].count()
    return "Comments count {}".format(count)


def main():
    for i in query_list:
        with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
            futures = []
            futures.append(executor.submit(get_data, q=i))
            for future in concurrent.futures.as_completed(futures):
                print(future.result())

if __name__ == '__main__':
    main()

