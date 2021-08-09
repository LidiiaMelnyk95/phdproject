import botometer
import pandas as pd

rapidapi_key = "1b47c699f8mshc1e15b6f0dc3ab7p1d8f63jsna0ae42e3ac74"
twitter_app_auth = {
    'consumer_key': 'eqSplDufO4H8eeDbaK0zpBt51',
    'consumer_secret': 'nAThDTE6G1DksGMoEPldY7CahOUQEDVYmdBlUWs9zkRliAKbeE',
    'access_token': '1333491145717010432-C7vpcGDqrVwp7sGyhnwwTj1Hzt8val',
    'access_token_secret': 'jrU7Ciy3bUXKVWg2QRRxU9XNrU8DShFvtMP0MS2OKAKgS'
  }

blt_twitter = botometer.Botometer(consumer_key=twitter_app_auth['consumer_key'], consumer_secret=twitter_app_auth['consumer_secret'],
                    access_token=twitter_app_auth['access_token'], access_token_secret= twitter_app_auth['access_token_secret'],
                    rapidapi_key=rapidapi_key)

df = pd.read_csv('/Users/lidiiamelnyk/Documents/Covid_tweets_tagung/corona infections 50 scrolls transformed.csv', sep = ',', encoding = 'utf-8-sig')
df['Author_Name'] = df['Author_Name'].astype(str)
for i, row in df.iterrows():
    blt_scores = []
    for k in row['Author_Name'].split('\n'):
        blt_score = blt_twitter.check_account(k)
        blt_score = round(blt_score['cap']['universal'],2)
        blt_scores.append(blt_score)
    df.loc[i, 'Bot_score'] = blt_scores

print(df.quantile(q=0.95, axis=df['Bot_score'], numeric_only=True, interpolation='linear'))
