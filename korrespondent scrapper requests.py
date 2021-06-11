import concurrent.futures
import json
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
theme_url_curfew = 'https://korrespondent.net/special/2095-karantyn-v-kyeve-y-ukrayne'
theme_url_covid = 'https://korrespondent.net/Default.aspx?page_id=60&lang=ru&stx=коронавирус&roi=0&st=1'
columns_names = 'url', 'comment', 'date', 'name'


def construct_topics_urls(url, max_range):
    topic_urls = []
    for i in range(0, 900):
        page_num = i + 1
        url_new = url + "&p=" + str(page_num)
        topic_urls.append(url_new)
    return topic_urls


def construct_news_urls(topic_urls):
    url_array = []
    for url in topic_urls:
        response = requests.get(url, timeout=60, verify=False)
        content = BeautifulSoup(response.content, "html.parser")
        main_div = content.find('div', attrs="articles-list")
        try:
            news_sections = main_div.find_all('div', attrs="article article_rubric_top")
        except AttributeError:
            print("Cannot find news_section")
            continue
        for news in news_sections:
            url_news = news.find('a').get('href')
            url_array.append(url_news)
            print("URL array length {}".format(len(url_array)))
    url_array = set(url_array)
    return url_array


class GetData:
    def __init__(self):
        self.url = 'https://cmt.korrespondent.net/comments/list.hnd'

    @staticmethod
    def get_info_id_from_url(url):
        info_id = re.findall("\d+", url)[0]
        return info_id

    def get_data(self, info_id):
        parameters = {"lotId": "10", "sort": 1, "page": 0, "size": 20, "callback": None, "infoId": info_id}
        response = requests.get(self.url, params=parameters, verify=False)
        return response.content.decode("utf-8")

    @staticmethod
    def parsing(text):
        json_string = text[1:-1]
        json_object = json.loads(json_string)
        comments_array = []
        for item in json_object["items"]:
            comments_array.append({"comment": item["text"], "username": item["userName"], "date": item["date"]})
        return comments_array


def get_texts_dataframe(url):
    data_getter = GetData()
    info_id = GetData.get_info_id_from_url(url)
    data_response = data_getter.get_data(info_id)
    data = GetData.parsing(data_response)
    rows = []
    df1 = pd.DataFrame(columns=columns_names)
    for item in data:
        rows.append({'url': url, 'comment': item['comment'], 'date': item['date'],
                     'name': item['username']})
    df1 = df1.append(rows, ignore_index=True)
    df1 = df1.drop_duplicates()
    return df1


def scrape_texts(url):
    df1 = get_texts_dataframe(url)
    count = df1['comment'].count()
    if count <= 0:
        return
    filename = "/Users/lidiiamelnyk/Documents/korrespondent/" + str(hash(url)) + '.csv'
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


def main():
    topic_urls = construct_topics_urls(theme_url_curfew, 1) + construct_topics_urls(theme_url_covid, 1)
    print("Topic URLs amount {}".format(len(topic_urls)))
    news_urls = construct_news_urls(topic_urls)
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
            futures = []
            for future_url in news_urls:
                futures.append(executor.submit(scrape_texts, url=future_url))
                for future in concurrent.futures.as_completed(futures):
                    print(future.result())
    except ConnectionError and ConnectionRefusedError:
        pass


if __name__ == '__main__':
    main()
