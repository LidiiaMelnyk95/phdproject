import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
urlpage = 'https://korrespondent.net/world/4361670-v-yndyy-nachaly-molytsia-bohyne-COVID'
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True
driver = webdriver.Firefox(executable_path= '/Users/lidiiamelnyk/Documents/korrespondent/geckodriver', options=fireFoxOptions)
driver.get(urlpage)
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var "
#                      "lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep for 3s
#time.sleep(15)
button = driver.find_element_by_css_selector('a[onclick="loadComments()"]')
button.click()
results = driver.find_element_by_xpath('//*[@id="frm"]/div[3]/div[1]/div[7]/div/div[2]/div[10]/div[3]/div/div/div[2]').text
name =  driver.find_element_by_xpath('//*[@id="frm"]/div[3]/div[1]/div[7]/div/div[2]/div[10]/div[3]/div/div/div[1]/a').text
date = driver.find_element_by_xpath('//*[@id="frm"]/div[3]/div[1]/div[7]/div/div[2]/div[10]/div[3]/div/div/div[1]').text[(len(driver.find_element_by_xpath('//*[@id="frm"]/div[3]/div[1]/div[7]/div/div[2]/div[10]/div[3]/div/div/div[1]').text) - 17):]

print('Text is: {}, '
      'name is : {}, '
      'date is: {}'.format(results,name,date))

driver.quit()