import concurrent.futures
import json
from fake_user_agent.main import user_agent
from user_agent import generate_user_agent, generate_navigator
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import pandas as pd
header = {
  'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'accept-encoding':'gzip, deflate, br',
  'accept-language':'ru-RU,ru;q=0.8,en-US;q=0.8,en;q=0.7',
  'cache-control':'no-cache',
  'dnt': '1',
  'pragma': 'no-cache',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

session = requests.Session()
session.headers = header
theme_url_curfew = 'https://censor.net/ua/theme/705/koronavirus_i_karantyn/news/page/'
columns_names = 'url', 'comment', 'date', 'name', 'readers'


def main():
    topic_urls = construct_topics_urls()
    print("Topic URLs amount {}".format(len(topic_urls)))
    url_array = []

    for url in topic_urls:
        response = session.get(url, headers= session.headers, timeout = 60)
        content = BeautifulSoup(response.content, "html.parser")
        main_div = content.find('div', attrs="curpane")
        news_sections = None
        try:
            news_sections = main_div.find_all('article', attrs="item")
        except AttributeError:
            print("Cannot find news_section")
            continue
        for news in news_sections:
            url_news = news.find('h3').find('a').get('href')
            if 'censor' not in url_news:
                url_news = 'https://censor.net' + url_news
            url_array.append(url_news)
            url_array = list(dict.fromkeys(url_array))
            print("URL array length {}".format(len(url_array)))
    url_array = set(url_array)
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        futures = []
        for future_url in url_array:
            futures.append(executor.submit(scrape_text, url=future_url))
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
                # for url_content in url_array:
                # scrape_text(url_content)

    # df2 = pd.read_csv('comments_new.csv', sep=',')


def construct_topics_urls():
    topic_urls = []
    for i in range(1, 700):
        page_num = i + 1
        url_new = theme_url_curfew + str(page_num)
        topic_urls.append(url_new)
    return topic_urls


def get_comments_text(url):
    response = session.get(url,headers = session.headers, timeout=60)
    content = BeautifulSoup(response.content, "html.parser")
    comment_text_array = []
    next_page_url = None
    comment_section = content.find('div', id='comments')
    comments_items_array = comment_section.find_all('div', attrs='item')
    next_page_url = comment_section.find('a', attrs='pag_next')
    for comment_item in comments_items_array:
        try:
            comment_text = comment_item.find('div', attrs='commtext comment_maxheight').get_text()
            comment_date = comment_item.find('div', attrs='comminfo').find('span', attrs='time').get_text()[:10]
            comment_author = comment_item.find('span', attrs='author')
            comment_author_page_url = comment_author.find('a').get('href')
            author_name = get_name(comment_author_page_url)
            author_readers = get_readers(comment_author_page_url)
            obj = {'comment': comment_text, 'date': comment_date, 'author_name': author_name, 'readers': author_readers}
            comment_text_array.append(dict(obj))
        except AttributeError:
            comment_text_array = []
    return comment_text_array, next_page_url


def scrape_text(url):
    init_url = url
    #print(init_url)
    comment_text_array = []
    while url is not None:
        comments, url = get_comments_text(url)
        comment_text_array = comment_text_array + comments
    rows = []
    df1 = pd.DataFrame(columns=columns_names)
    for item in comment_text_array:
        rows.append({'url': init_url, 'comment': item.get('comment'), 'date': item.get('date'),
                     'name': item.get('author_name'), 'readers': item.get('readers')})
    df1 = df1.append(rows, ignore_index=True)
    df1 = df1.drop_duplicates()
    filename = "/Users/lidiiamelnyk/Documents/comments_folder/" + str(hash(init_url)) + '.csv'
    with open(filename, 'w+', encoding='utf-8-sig',newline='') as file:
        df1.to_csv(file, sep=',', na_rep='', float_format=None,
                    columns=['url', 'comment', 'date', 'name', 'readers'],
                    header=True, index=False, index_label=None,
                    mode='a', compression='infer',
                    quoting=None, quotechar='"', line_terminator=None, chunksize=None,
                    date_format=None, doublequote=True, escapechar=None, decimal='.')
    print("Finished writing to {}".format(filename))
    file.close()
    count = df1['comment'].count()
    return "Comments count {}".format(count)

def get_name(url):
    response = session.get(url,headers = session.headers, timeout=60)
    content = BeautifulSoup(response.content, "html.parser")
    author_profile = content.find('div', attrs='wrap')
    author_profile_main = author_profile.find('div', attrs='profile_main')
    name = author_profile_main.find('div', attrs='name').find('a').get_text()
    return name


def get_readers(url):
    response = session.get(url,headers = session.headers, timeout=60)
    content = BeautifulSoup(response.content, "html.parser")
    author_profile = content.find('div', attrs='wrap')
    author_profile_main = author_profile.find('div', attrs='profile_main')
    readers = author_profile_main.find_all('div', attrs='fval')
    reading_me = 0
    i_am_reading = 0
    for div in readers:
        contents = str(div)
        if 'Меня читают' in contents:
            try:
                reading_me = div.find('a').get_text()
            except AttributeError:
                pass
        elif 'Я читаю' in contents:
            try:
                i_am_reading = div.find('a').get_text()
            except AttributeError:
                pass
    comment_author_readers_array = {'reading_me': reading_me, 'i_am_reading': i_am_reading}
    return json.dumps(comment_author_readers_array)


if __name__ == '__main__':
    main()
    # while True:
    #    main()
    #    time.sleep(3600)
