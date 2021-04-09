from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

def notify_about_detection():
    for i in range(10):
        os.system('aplay beep.wav')
        time.sleep(1)


def get_source_code(query):
    url = 'https://www.bloomberg.com/search?query={}'.format(query)
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(15)
    # in case of bot detection
    soup = BeautifulSoup(driver.page_source)
    bot_detection = soup.find('title').text
    while bot_detection == 'Bloomberg - Are you a robot?':
        notify_about_detection()
        time.sleep(60)
        # while verifying that we are not bot
        soup = BeautifulSoup(driver.page_source)
        bot_detection = soup.find('title').text
    # clicking 99 times button "load more"
    page_num = 1
    while page_num != 100:
        try:
            driver.find_element_by_class_name('loadMoreButtonContainer__e27276de').click()
        except:
            break
        time.sleep(2)
        page_num += 1

    return driver.page_source

def parse_source_code(source_code, query):
    soup = BeautifulSoup(source_code)
    news_list = soup.find_all('div', {'class': 'text__1793994f withThumbnail__deb7b221'})

    result_list = []
    for news in news_list:
        href = news.find('a', {'class': 'headline__55bd5397'}).get('href')
        headline = news.find('a', {'class': 'headline__55bd5397'}).text
        if news.find('div', {'class': 'authors__70a84826'}):
            author = news.find('div', {'class': 'authors__70a84826'}).text
        else:
            author = 'none'
        if news.find('a', {'class': 'summary__bbda15b4'}):
            summary = news.find('a', {'class': 'summary__bbda15b4'}).text
        else:
            summary = 'none'
        date = news.find('div', {'class': 'publishedAt__79f8aaad'}).text

        result_list.append({
            'date': date,
            'headline': headline,
            'link': href,
            'author': author,
            'summary': summary
        })

    pandas_dataframe = pd.DataFrame(result_list)
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/bloomberg'):
        os.makedirs('data/bloomberg')
    pandas_dataframe.to_csv('data/bloomberg/{}.csv'.format(query))

def parser(query_list):
    for query in query_list:
        source_code = get_source_code(query)
        parse_source_code(source_code, query)