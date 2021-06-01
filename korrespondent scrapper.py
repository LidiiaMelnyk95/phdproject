import concurrent.futures
import json

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import socket
import requests
from lxml.html import fromstring
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

proxies = get_proxies()


main_url= 'https://korrespondent.net/Default.aspx?page_id=60&lang=ru&stx=коронавирус&roi=93&st=1'
columns_names = 'url', 'comment', 'date', 'name', 'readers'
def wait_on_b():
    time.sleep(10)
    return 10


def main():
    topic_urls = construct_topics_urls()
    #print("Topic URLs amount {}".format(len(topic_urls)))
    url_array = []

    for url in topic_urls:
        response = requests.get(url, timeout=60)
        content = BeautifulSoup(response.content, "html.parser")
        main_div = content.find('div', attrs="articles-list")
        news_sections = None
        try:
            news_sections = main_div.find_all('div', attrs="article article_rubric_top")
        except AttributeError:
            print("Cannot find news_section")
            continue
        for news in news_sections:
            url_news = news.find('a').get('href')
            #if 'censor' not in url_news:
            #    url_news = 'https://censor.net' + url_news
            url_array.append(url_news)
            url_array = list(dict.fromkeys(url_array))
            print("URL array length {}".format(len(url_array)))
    url_array = set(url_array)
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
            futures = []
            for future_url in url_array:
                futures.append(executor.submit(scrape_text, url=future_url))
                for future in concurrent.futures.as_completed(futures):
                 #   time.sleep(5)
                    print(future.result())
    except ConnectionError and ConnectionRefusedError:
        pass
                # for url_content in url_array:
                # scrape_text(url_content)

    # df2 = pd.read_csv('comments_new.csv', sep=',')


def construct_topics_urls():
    topic_urls = []
    for i in range(0, 321):
        page_num = i + 1
        url_new = main_url + '&p=' + str(page_num)
        topic_urls.append(url_new)
    return topic_urls


def get_comments_text(url):
    response = requests.get(url, timeout=60)
    content = BeautifulSoup(response.content, "html.parser")
    comment_text_array = []
    next_page_url = None
    try:
        comment_section = content.find('div', attrs ='comments')
        comments_items_array = comment_section.find_all('div', attrs='comments_list')
        next_page_url = comment_section.find('a', attrs='pag_next')
        for comment_item in comments_items_array:
            comment_text = comment_item.find('div', attrs='comment-item__text').get_text()
            comment_date = comment_item.find('div', attrs='comment-item__top').find('span', attrs = 'comment_ip').get('/a')[:10]
            comment_author = comment_item.find('div', attrs='comment-item__top')
            comment_author_page_url = comment_author.find('a').get('href')
            obj = {'comment': comment_text, 'date': comment_date}
            comment_text_array.append(dict(obj))
            print(comment_text_array)
    except AttributeError:
        comment_text_array = []
    return comment_text_array, next_page_url


def scrape_text(url):
    init_url = url
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
    filename = "/Users/lidiiamelnyk/Documents/comments_korrespondent/" + str(hash(init_url)) + '.csv'
    with open(filename, 'w+', encoding='utf-8-sig',
              newline='') as file:
        df1.to_csv(file, sep=',', na_rep='', float_format=None,
                   columns=['url', 'comment', 'date', 'name', 'readers'],
                   header=True, index=False, index_label=None,
                   mode='a', compression='infer',
                   quoting=None, quotechar='"', line_terminator=None, chunksize=None,
                   date_format=None, doublequote=True, escapechar=None, decimal='.')
        print("Finished writing to {}".format(filename))
        file.close()
    count = df1['comment'].count()
    #return "Comments count {}".format(count)

'''
def get_name(url):
    response = requests.get(url, timeout=60)
    content = BeautifulSoup(response.content, "html.parser")
    author_profile = content.find('div', attrs='wrap')
    author_profile_main = author_profile.find('div', attrs='profile_main')
    name = author_profile_main.find('div', attrs='name').find('a').get_text()
    return name


def get_readers(url):
    response = requests.get(url, timeout=60)
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

'''
if __name__ == '__main__':
    main()
    #while True:
     #   main()
      #  time.sleep(120)
