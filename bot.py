import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import pickle
import os

headers = {'User-Agent': 'Chrome/89.0.4389.82'}

def lancers_data():
    base = 'https://www.lancers.jp'
    url = base + '/work/search?open=1&keyword=%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0'
    res = requests.get(url, headers=headers)
    soup = bs(res.text,'html.parser')
    cards = soup.select('div.c-media-list__item.c-media')
    ads = soup.select('div.c-media-list__item.c-media.c-media--clickable') # 求人広告
    cards = [card for card in cards if card not in ads]    
    data = []
    for card in cards:
        sleep(1)
        url = base + card.select_one('a[class="c-media__title"]').get('href')
        title = card.select_one('.c-media__title-inner').text.split('\n')[-2].replace(' ', '')
        price = card.select_one('.c-media__job-price').text.replace('\n', '').split('/')[0]
        # detail = get_detail(url)
        d = (title, price, url)
        data.append(d)
    return data

def crowdworks_data():
    base = 'https://crowdworks.jp'
    url = base + '/public/jobs/search?keep_search_criteria=true&order=score&hide_expired=true&search%5Bkeywords%5D=%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0'
    res = requests.get(url, headers=headers)
    soup = bs(res.text,'html.parser')
    lists = soup.select('#result_jobs > .search_results > ul > li')
    data = []
    for l in lists:
        title = l.select_one('.item_title').text.replace('\n', '')
        url = base + l.select_one('.item_title > a').get('href')
        price = l.select_one('b.amount').text.replace('\n', '').replace(' ', '')
        data.append((title, price, url))
    return data

def coconala_data():
    base = 'https://coconala.com'
    url = base + '/requests?keyword=%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0&recruiting=true&page=1'
    res = requests.get(url, headers=headers)
    soup = bs(res.text,'html.parser')
    lists = soup.select('#result_jobs > .search_results > ul > li')
    ls = soup.select('div.c-searchPage_itemList > div > a')
    data = []
    for l in ls:
        a = l.select_one('div > div > div.c-itemInfo_title > a')
        title = a.text.replace('\n', '').replace(' ', '')
        price = l.select_one('div > div > div > div > div > div > div').text.replace('\n', '').replace(' ', '')
        url = a.get('href')
        data.append((title,price,url))
    return data


def send_message(jobs):
    webhook = os.environ["SLACK_WEBHOOK_TEST"]
    json = "{'text' : '%s'}"
    text = "依頼 : %s\n報酬 : %s\nurl : %s"
    for job in jobs:
        requests.post(webhook, data=(json % ('-------------------------')))    
        title, price, url = job
        data = json % (text % (title, price, url))
        requests.post(webhook, data=data.encode('utf-8'))
        
        
def write_cache(data):
    with open('cache.pkl', 'wb') as cache:
        pickle.dump(data , cache)

def read_cache():
    with open('cache.pkl', 'rb') as cache:
        return pickle.load(cache)

def main():
    data = lancers_data()
    data.extend(crowdworks_data())
    data.extend(coconala_data())
    cache = read_cache()
    print('------ole cache------')
    for c in cache:        
        print(c[0])
    diff = [d for d in data if d not in cache]
    send_message(diff)
    write_cache(data)
    print('------new cache------')
    for c in read_cache():
        print(c[0])    
if __name__ == '__main__':
    main()