import concurrent.futures

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import json

topic_urls = []
i = 1

theme_url_curfew = 'https://korrespondent.net/special/2095-karantyn-v-kyeve-y-ukrayne'
theme_url_covid = 'https://korrespondent.net/Default.aspx?page_id=60&lang=ru&stx=коронавирус&roi=0&st=1'
columns_names = 'url', 'comment', 'date', 'name'

                # for url_content in url_array:
                # scrape_text(url_content)

    # df2 = pd.read_csv('comments_new.csv', sep=',')

def construct_topics_urls(url, max_range):
    topic_urls = []
    for i in range(0, max_range):
        page_num = i + 1
        url_new = url + "&p=" + str(page_num)
        topic_urls.append(url_new)
    return topic_urls



def main():
    topic_urls = construct_topics_urls(theme_url_curfew, 147) + construct_topics_urls(theme_url_covid, 825)
    print("Topic URLs amount {}".format(len(topic_urls)))
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
            url_array.append(url_news)
            #url_array = list(dict.fromkeys(url_array))
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


class GetData():
    def __init__(self, url, info_id, text, comments, author, date):
        self.url = 'https://cmt.korrespondent.net/comments/list.hnd'
        self.info_id = self.get_info_id_from_url( )
        self.text = self.get_data( )

    def init_url(self, url):
        url = 'https://cmt.korrespondent.net/comments/list.hnd'
        return url
    def get_info_id_from_url(self, url):
        info_id = re.findall("\d+", url)[0]
        return info_id

    def get_data(self, info_id):
        parameters = {"lotId": "10", "sort": 1, "page": 0, "size": 20, "callback": None, "infoId": info_id}
        response = requests.get(self.url, params=parameters)
        return response.content.decode("utf-8")

    def parsing(self, text):
        json_string = text[1:-1]
        json_object = json.loads(json_string)
        comments_array = []
        for item in json_object["items"]:
            comments_array.append({"comment": item["text"], "username": item["userName"], "date": item["date"]})
        return comments_array

def scrape_text(url):
    info_id = GetData.get_info_id_from_url(url)
    data_request = GetData.get_data(info_id)
    comments = GetData.parsing(data_request).get('comment')
    author_name = GetData.parsing(data_request).get('username')
    date = GetData.parsing(data_request).get('date')
    rows = []
    df1 = pd.DataFrame(columns=columns_names)
    rows.append({'url': url, 'comment': comments, 'date': date,
                     'name': author_name})
    df1 = df1.append(rows, ignore_index=True)
    df1 = df1.drop_duplicates()
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


if __name__ == '__main__':
    main()