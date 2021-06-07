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
        try:
            news_sections = main_div.find_all('div', attrs="article article_rubric_top")
        except AttributeError:
            print("Cannot find news_section")
            continue
        for news in news_sections:
            url_news = news.find('a').get('href')
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


class GetData():
    def __init__(self, url, info_id, text):
        self.url = 'https://cmt.korrespondent.net/comments/list.hnd'
        self.info_id = self.get_info_id_from_url( )
        self.text = self.get_data( )

    def get_info_id_from_url(url):
        info_id = re.findall("\d+", url)[0]
        return info_id

    def get_data(info_id):
        parameters = {"lotId": "10", "sort": 1, "page": 0, "size": 20, "callback": None, "infoId": info_id}
        response = requests.get(url, params=parameters)
        return response.content.decode("utf-8")

    def parsing(text):
        json_string = text[1:-1]
        json_object = json.loads(json_string)
        comments_array = []
        for item in json_object["items"]:
            comments_array.append({"comment": item["text"], "username": item["userName"], "date": item["date"]})
        return comments_array


if __name__ == '__main__':
    main()