from scrape import get_data
from cache import mkDiff, updateCache
import os
import requests


def send_message(data):
    webhook = os.environ["SLACK_WEBHOOK_TEST"]
    json = "{'text' : '%s'}"
    text = "依頼 : %s\n報酬 : %s\nurl : %s"
    for d in data:
        requests.post(webhook, data=(json % ('-------------------------')))    
        title, price, url = d
        data = json % (text % (title, price, url))
        requests.post(webhook, data=data.encode('utf-8'))              

def main():
    data = get_data()
    diff = mkDiff(data)
    send_message(diff)
    updateCache(data)  

def main():
    data = lancers_data()
    data.extend(crowdworks_data())
    data.extend(coconala_data())
    data = cleansing(data)
    cache = read_cache()    
    diff = [d for d in data if d not in cache]
    for c in diff:        
        print(c[0])
    send_message(diff)
    write_cache(data)  
    
if __name__ == '__main__':
    main()