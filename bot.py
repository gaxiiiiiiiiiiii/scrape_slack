from scrape import get_offers
from cache import take_diff, update_cache
import os
import requests

def send_message(message):
    webhook = os.environ["SLACK_WEBHOOK_TEST"]
    base = "{'text' : '%s'}"
    data = base % message
    requests.post(webhook, data=data.encode('utf-8'))

    
def send_offers(offers):
    base = "依頼 : %s\n報酬 : %s\nurl : %s"
    for offer in offers:
        send_message('-------------------------')
        message = base % offer
        send_message(message)
    

    
if __name__ == '__main__':
    offers = get_offers()
    diff = take_diff(offers)
    send_offers(diff)
    update_cache(offers)  