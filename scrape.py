import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import os
from urllib.parse import urljoin

headers = {'User-Agent': 'Chrome/89.0.4389.82'}

LANCERS_URL = 'https://www.lancers.jp/work/search?open=1&keyword=%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0'
CROWDDWORKS_URL = 'https://crowdworks.jp/public/jobs/search?keep_search_criteria=true&order=score&hide_expired=true&search%5Bkeywords%5D=%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0'
COCONALA_URL = 'https://coconala.com/requests?keyword=%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0&recruiting=true&page=1'


####################
#      base        #
####################

def get_soup(url):    
    try:        
        res = requests.get(url, headers=headers)
        soup = bs(res.text,'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print("request error : ",e)

def make_parser(base_url, base_parser):
    def parser(elm):
        title, price, parmalink = base_parser(elm)
        url = urljoin(base_url, parmalink)
        return (title, price, url)
    return parser

def get_offer(url, get_elms, base_parser):
    soup = get_soup(url)
    elms = get_elms(soup)
    parser = make_parser(url, base_parser)    
    offers = list(map(parser, elms))
    return offers  


def get_offers():
    lancers    = get_offer(LANCERS_URL,     get_lancers_elms,    lancers_parser)
    crowdworks = get_offer(CROWDDWORKS_URL, get_crowdworks_elms, crowdworks_parser)
    coconala   = get_offer(COCONALA_URL,    get_coconala_elms,   coconala_parser)
    offers = lancers + crowdworks + coconala
    return offers


####################
#     lancers      #
####################

def get_lancers_elms(soup):
    elms = soup.select('div.c-media-list__item.c-media')
    ads = soup.select('div.c-media-list__item.c-media.c-media--clickable') # 求人広告
    diff = list(set(elms) - set(ads))
    return diff

def lancers_parser(elm):    
    title = elm.select_one('.c-media__title-inner').text.split('\n')[-2].replace(' ', '')
    price = elm.select_one('.c-media__job-price').text.replace('\n', '').split('/')[0].replace(' ', '')
    parmalink = elm.select_one('a.c-media__title').get('href')
    return (title, price, parmalink)


####################
#    crowdworks    #
####################

def get_crowdworks_elms(soup):
    elms = soup.select('#result_jobs > .search_results > ul > li')
    return elms

def crowdworks_parser(elm):
    title = elm.select_one('.item_title').text.replace('\n', '').replace(' ', '')    
    price = elm.select_one('b.amount').text.replace('\n', '').replace(' ', '')
    parmalink = elm.select_one('.item_title > a').get('href')
    return (title, price, parmalink)


####################
#     coconala     #
####################

def get_coconala_elms(soup):
    elms = soup.select('div.c-searchPage_itemList > div > a')
    return elms

def coconala_parser(elm):
    a = elm.select_one('div > div > div.c-itemInfo_title > a')
    title = a.text.replace('\n', '').replace(' ', '')
    price = elm.select_one('div > div > div > div > div > div > div').text.replace('\n', '').replace(' ', '')
    url = a.get('href')
    return (title, price, url)


