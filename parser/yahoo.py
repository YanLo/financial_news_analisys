from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

def get_source_code(query):
    url = 'https://finance.yahoo.com/quote/{0}/news?p={0}'.format(query)
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(30)

    return driver.page_source

def parce_source_code(source_code, query):
    soup = BeautifulSoup(source_code)
    news_list = soup.find_all('li', {'class': 'js-stream-content Pos(r)'})

    result_list = []
    for news in news_list[2:]:
        headline = news.find('h3').text
        summary = news.find('p').text
        source_and_date = news.find('div', {'class': 'C(#959595) Fz(11px) D(ib) Mb(6px)'}).find_all('span')
        source = source_and_date[-2].text
        date = source_and_date[-1].text

        result_list.append({
            'date': date,
            'headline': headline,
            'summary': summary,
            'source': source
        })

    pandas_dataframe = pd.DataFrame(result_list)
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/yahoo'):
        os.makedirs('data/yahoo')
    pandas_dataframe.to_csv('data/yahoo/{}.csv'.format(query))

def parser(query_list):
    for query in query_list:
        source_code = get_source_code(query)
        parce_source_code(source_code, query)