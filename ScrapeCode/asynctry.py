from mydict import MyDict
import asyncio
import aiohttp
import random
from flipscrape import Product
import flask
import time
import requests

p = Product('http://www.flipkart.com/redmi-1s/p/itmdz6zpuatkgfjp?pid=MOBDZ6Y3CK65QFZY',30)
app = flask.Flask(__name__)

@asyncio.coroutine
def get_url(url):
    wait_time = random.randint(1, 4)
    #yield from asyncio.sleep(wait_time)
    print('Done: URL {} took {}s to get!'.format(url, wait_time))
    resp = requests.get(url)
    return resp.text


@asyncio.coroutine
def process_as_results_come_in():
    coroutines = [get_url(url) for url in p.make_url_list()]
    resp_lis = []
    for coroutine in asyncio.as_completed(coroutines):
        resp = yield from coroutine
        print (resp.text)
        #print('Coroutine for {} is done'.format(url))

@asyncio.coroutine
def process_once_everything_ready():
    
    coroutines = [get_url(url) for url in p.make_url_list()]
    results = yield from asyncio.gather(*coroutines)
    


def main():
    res = []
    loop = asyncio.get_event_loop()
    #print("First, process results as they come in:")
    loop.run_until_complete(process_as_results_come_in())
    print("\nNow, process results once they are all ready:")
    #loop.run_until_complete(process_once_everything_ready())
    print ('dfas')
   


if __name__ == '__main__':
    main()