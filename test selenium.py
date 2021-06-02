import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
urlpage = 'https://korrespondent.net/world/4361670-v-yndyy-nachaly-molytsia-bohyne-COVID'
driver = webdriver.Firefox(executable_path= '/Users/lidiiamelnyk/Documents/korrespondent/geckodriver')
driver.get(urlpage)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var "
                      "lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep for 30s
time.sleep(30)
results = driver.find_element_by_xpath('//*[@id="frm"]/div[3]/div[1]/div[7]/div/div[2]/div[10]/div[3]/div/div/div[2]').text
print(results)