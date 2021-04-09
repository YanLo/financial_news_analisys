from lxml import html, etree
import requests
import pandas as pd
import regex
import os

def get_source_code(url, session):
    response = session.get(url)
    return response.text

def save_text(text, filename):
    with open(filename, 'w') as output:
        output.write(text)

def read_text(filename):
    with open(filename, 'r') as input_:
        text = input_.read()
    return text

def extract_headlines(url, session, news_list):
    text = get_source_code(url, session)
    tree = html.fromstring(text)
    headlines = tree.xpath('.//div[@class = "searchresult"]/a/text()')
    dates = tree.xpath('.//div[@class="deemphasized"]/span/text()')
    links = tree.xpath('.//div[@class = "searchresult"]/a/@href')

    for headline, date, link in zip(headlines, dates, links):
        news_list.append({
            'date': date,
            'headline': headline,
            'link': link
        })

    return len(headlines)

def load_news(url_first_page, session):
    news_list = []
    extract_headlines(url=url_first_page, session=session, news_list=news_list)
    print('Loaded headlines: ', len(news_list), flush=True)

    num = 1
    news_quantity = 100
    while news_quantity < 1000:
        current_page_url = url_first_page + '&o={}'.format(num * 100 + 1)
        headlines_num = extract_headlines(url=current_page_url, session=session, news_list=news_list)
        num += 1
        news_quantity += headlines_num
        if (headlines_num == 0):
            break
        print('Loaded headlines: ', len(news_list), flush=True)

    return pd.DataFrame(news_list)


def parser(tegs_list):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'
    })

    for teg in tegs_list:
        teg_url = 'https://www.marketwatch.com/search?q={}&m=Keyword&rpp=100&mp=159&bd=false&rs=true'.format(teg)
        print('----Loading for', teg)
        teg_pandas_dataframe = load_news(url_first_page=teg_url, session=session)

        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists('data/marketwatch'):
            os.makedirs('data/marketwatch')
        teg_pandas_dataframe.to_csv('data/marketwatch/{}.csv'.format(teg))

    print('-------Loading finished-------')