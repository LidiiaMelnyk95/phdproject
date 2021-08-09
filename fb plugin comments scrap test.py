import concurrent.futures

import pandas as pd
import requests
from bs4 import BeautifulSoup

topic_urls = []
i = 1

theme_url_vaccination = 'https://zn.ua/theme/14786/'
theme_url_curfew = 'https://zn.ua/theme/74/'
theme_url_corona_world = 'https://zn.ua/theme/69/'
columns_names = 'url', 'comment', 'date', 'name'


def construct_topics_urls():
    topic_urls = []
    for i in range(1, 100):
        url = theme_url_corona_world
        page_num = i + 1
        url_new = url + 'p' + str(page_num)
        topic_urls.append(url_new)
    for i in range(1, 100):
        url = theme_url_curfew
        page_num = i + 1
        url_new = url + 'p' + str(page_num)
        topic_urls.append(url_new)
    for i in range(1, 100):
        url = theme_url_vaccination
        page_num = i + 1
        url_new = url + 'p' + str(page_num)
        topic_urls.append(url_new)
    return topic_urls


def main():
    topic_urls_main = construct_topics_urls()
    print("Topic URLs amount {}".format(len(topic_urls_main)))
    url_array = []
    for url in topic_urls_main:
        response = requests.get(url, timeout=60)
        content = BeautifulSoup(response.content, "html.parser")
        main_div = content.find('div', attrs='sbody')\
            .find('div', id="container")\
            .find('div', id='holder')\
            .find('div', id='left')
        try:
            news_sections = main_div.find('div', attrs="left_news_list section").find('ul', attrs='news_list').find_all(
                'li')
            for news in news_sections:
                url_new = news.find('a').get('href')
                url_news = 'https://zn.ua' + url_new
                url_array.append(url_news)
                url_array = list(dict.fromkeys(url_array))
                print("URL array length {}".format(len(url_array)))
        except AttributeError:
            print("Cannot find news_section")
            continue
    url_array = set(url_array)
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
            futures = []
            for future_url in url_array:
                futures.append(executor.submit(scrape_text, url=future_url))
                for future in concurrent.futures.as_completed(futures):
                    #   time.sleep(5)
                    if future.result():
                        print(future.result())
    except Exception as e:
        print(e)


def request_comment_data(url, page=1):
    response = requests.get(url, timeout=30)
    content = BeautifulSoup(response.content, "html.parser")
    try:
        article = content.find('div', attrs="comment_block_art")\
                        .find('div', attrs="comments_list")\
                        .find('ul', attrs="main_comments_list")['data-absnum']
        try:
            x = requests.post(url='https://zn.ua/actions/comments/',
                              data={'article': article, 'page': page, 'typeload': 4, 'comtype': 1}).json()
        except:
            myobj = {'article': article, 'page': 1, 'typeload': 1, 'comtype': 1}
            x = requests.post(url='https://zn.ua/actions/comments/', data=myobj).json()
        json_file = x
    except AttributeError and ValueError:
        return None
    if json_file['comments']['success']:
        return json_file
    else:
        print('No comments found here')
        return None


def get_comments_text(url):
    file = request_comment_data(url)
    if file is None:
        return [], None
    pages_count = file['comments']['result']['pages']
    comment_array = []
    page_counter = 1
    while page_counter <= pages_count:
        to_parse = file['comments']['result']['html']
        content = BeautifulSoup(to_parse, "html.parser")
        parsed_comment = content.find_all('li', attrs='comment_item')
        try:
            for comment in parsed_comment:
                comment_text = comment.find('span', attrs='comment_text_block').find('span',
                                                                                     attrs='comment_txt').get_text()
                parsed_name = comment.find('span', attrs='user_info_block').find('span',
                                                                                 attrs='user_nickname').get_text()
                parsed_date = comment.find('span', attrs='user_info_block').find('span',
                                                                                 attrs='comment_time').get_text()
                obj = {'comment': comment_text, 'date': parsed_date, 'author_name': parsed_name}
                comment_array.append(dict(obj))
        except AttributeError:
            comment_array = []
        page_counter += 1
        file = request_comment_data(url, page_counter)
    return comment_array, None


def scrape_text(url):
    init_url = url
    # print(init_url)
    comment_array = []
    while url is not None:
        comments, url = get_comments_text(url)
        comment_array = comment_array + comments
    rows = []
    df1 = pd.DataFrame(columns=columns_names)
    for item in comment_array:
        rows.append({'url': init_url, 'comment': item.get('comment'), 'date': item.get('date'),
                     'name': item.get('author_name')})
    df1 = df1.append(rows, ignore_index=True)
    df1 = df1.drop_duplicates()
    count = df1['comment'].count()
    if count <= 0:
        return
    filename = "/Users/lidiiamelnyk/Documents/comments_zn_ua/" + str(hash(init_url)) + '.csv'
    with open(filename, 'w+', encoding='utf-8-sig',
              newline='') as file:
        df1.to_csv(file, sep=',', na_rep='', float_format=None,
                   columns=['url', 'comment', 'date', 'name'],
                   header=True, index=False, index_label=None,
                   mode='a', compression='infer',
                   quoting=None, quotechar='"', line_terminator=None, chunksize=None,
                   date_format=None, doublequote=True, escapechar=None, decimal='.')
        print("Finished writing to {}".format(filename))
        file.close()
    return "Comments count {}".format(count)


if __name__ == '__main__':
    try:
        main()
    except ConnectionResetError:
        pass
    # while True:
    #   main()
    #  time.sleep(120)
