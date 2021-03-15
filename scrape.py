import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import os
from urllib.parse import urljoin

headers = {'User-Agent': 'Chrome/89.0.4389.82'}





def get_lancers_offer():
    search_url = 'https://www.lancers.jp/work/search?open=1&keyword=%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0'
    res = requests.get(search_url, headers=headers)
    soup = bs(res.text,'html.parser')
    offer_elms = soup.select('div.c-media-list__item.c-media')
    ads = soup.select('div.c-media-list__item.c-media.c-media--clickable') # 求人広告
    offer_elms = [offer for offer in offer_elms if offer not in ads]    
    offers = []
    for offer_elm in offer_elms:
        parma_link = offer_elm.select_one('a.c-media__title').get('href')
        url = urljoin(search_url, parma_link)
        title = offer_elm.select_one('.c-media__title-inner').text.split('\n')[-2].replace(' ', '')
        price = offer_elm.select_one('.c-media__job-price').text.replace('\n', '').split('/')[0].replace(' ', '')
        offers.append((title, price, url))
    return offers

def get_crowdworks_offer():
    search_url = 'https://crowdworks.jp/public/jobs/search?keep_search_criteria=true&order=score&hide_expired=true&search%5Bkeywords%5D=%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0'
    res = requests.get(search_url, headers=headers)
    soup = bs(res.text,'html.parser')
    offer_elms = soup.select('#result_jobs > .search_results > ul > li')
    offers = []
    for offer_elm in offer_elms:
        title = offer_elm.select_one('.item_title').text.replace('\n', '').replace(' ', '')
        parma_link = offer_elm.select_one('.item_title > a').get('href')
        url = urljoin(search_url, parma_link)
        price = offer_elm.select_one('b.amount').text.replace('\n', '').replace(' ', '')
        offers.append((title, price, url))
    return offers

def get_coconala_offer():
    base = 'https://coconala.com'
    search_url = base + '/requests?keyword=%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0&recruiting=true&page=1'
    res = requests.get(search_url, headers=headers)
    soup = bs(res.text,'html.parser')
    offer_elms = soup.select('div.c-searchPage_itemList > div > a')
    offers = []
    for offer_elm in offer_elms:
        a = offer_elm.select_one('div > div > div.c-itemInfo_title > a')
        title = a.text.replace('\n', '').replace(' ', '')
        price = offer_elm.select_one('div > div > div > div > div > div > div').text.replace('\n', '').replace(' ', '')
        url = a.get('href')
        offers.append((title,price,url))
    return offers

def get_offers():
    offers = get_lancers_offer()
    offers.extend(get_crowdworks_offer())
    offers.extend(get_coconala_offer())
    return offers
