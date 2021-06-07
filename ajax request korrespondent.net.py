import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
from lxml import etree
from bs4 import BeautifulSoup
import requests
urlpage = 'https://korrespondent.net/world/4361670-v-yndyy-nachaly-molytsia-bohyne-COVID'
response = urllib.request.urlopen(urlpage).read().decode("utf-8",'ignore')
html_structure = etree.HTML(response)

response_div = requests.get(urlpage, timeout=60)
content = BeautifulSoup(response_div.content, "html.parser")


def get_comment_text_if_exists(xpath):
    """Extracts a field by a CSS selector if exists."""
    try:
        return html_structure.xpath(xpath).text
    except NoSuchElementException:
        return ""


def get_author_name_if_existst(xpath):
    try:
        return html_structure.xpath(xpath).text
    except NoSuchElementException:
        return ""

def get_comment_date_if_existst(xpath):
    try:
        return html_structure.xpath(xpath)
    except NoSuchElementException:
        return ""


fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True
driver = webdriver.Firefox(executable_path= '/Users/lidiiamelnyk/Documents/korrespondent/geckodriver', options=fireFoxOptions)
driver.get(urlpage)
time.sleep(10)
# select the first suggestion from a suggestion dropdown

try:
    button = driver.find_element_by_css_selector('a[onclick="loadComments()"]')
    button.click()
    text = get_comment_text_if_exists('//*[@id="frm"]/div[3]/div[1]/div[7]/div/div[2]/div[10]/div[3]/div/div/div[2]')
    author_name = get_author_name_if_existst( '//*[@id="frm"]/div[3]/div[1]/div[7]/div/div[2]/div[10]/div[3]/div/div/div[1]/a')
    date = get_comment_date_if_existst( "//*[@id='frm']/div[3]/div[1]/div[7]/div/div[2]/div[10]/div[3]/div/div/div[1]').text[(len(driver.find_element_by_xpath('//*[@id='frm']/div[3]/div[1]/div[7]/div/div[2]/div[10]/div[3]/div/div/div[1]').text) - 17):]")
except:
    pass