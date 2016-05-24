import math
import pickle
from mydict import MyDict
import asyncio
import aiohttp
import bs4
import tqdm
import re
from naivesen import *
from flipscrape import *
import flask
import time
import requests

from bs4 import BeautifulSoup

import math


p = Product('http://www.flipkart.com/redmi-1s/p/itmdz6zpuatkgfjp?pid=MOBDZ6Y3CK65QFZY',800)
#p = Product('http://www.flipkart.com/moto-g-3rd-generation/p/itme9ysjr7mfry3n?pid=MOBE6KK93JG5WKB2&otracker=hp_2_Worth%20every%20penny_link_3_PMU',800)
n = NaiveBayes()


@asyncio.coroutine
def get(url):
    resp = yield from aiohttp.request('GET', url)
    if resp.status == 200:
#    resp = requests.get(*args, **kwargs)
#    return resp.text
        return (yield from resp.read())


@asyncio.coroutine
def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        yield from f

def get_analysis(txt):
    txt = txt.strip()
    txt = txt.lower()
    txt = txt.split('.')
    #txt = re.split('[\n.]',txt)
    #txt = [t.strip() for t in txt]
    sent_attrib = {'Cam':['camera','pics','photo','selfie'],'Perf':['perfomance','cpu','response', 'processing', 'processor','speed','gaming','ram','speed'],
        'Bat':['power', 'life', 'battery','backup','charging','standup'], 'Vfm':['price','cost','value','money'],
        'Serv':['service','delivery', 'replacement','delay','defective'],'Disp':['display','screen','resolution','gorilla','corning']}
    sent = {'Perf':0,'Bat':0,'Vfm':0,'Cam':0,'Serv':0,'Disp':0,'Overall':0}
    overall = 0
    for line in txt:
        sent_line = n.classify(line)
        for key in sent_attrib.keys():
            for attrib in sent_attrib[key]:
                if attrib in line:
                    sent[key] += sent_line
                    print (type(sent_line))
                    break
        sent['Overall'] += sent_line
    return sent

analysis = []

def first_magnet(page):
    global analysis
    soup = bs4.BeautifulSoup(page)
    dates = soup.findAll('div', {'class':'date line fk-font-small'})
    tests = soup.findAll('span', {'class':'review-text'})
    for date, test in zip(dates, tests):
        date = date.text
        date = date.strip()
        test = test.text
        test = test.strip()
        analysis.append([date,get_analysis(test)])
    pickle.dump(analysis, open(str(p.pname),'wb'))
    print (analysis)
    #a = soup.find('a', title='Download this torrent using magnet')
    


@asyncio.coroutine
def print_magnet(query):
    url = query
    #url = 'http://thepiratebay.se/search/{}/0/7/0'.format(query)
    #page = requests.request('GET',url)
    page = yield from get(url)
    magnet = first_magnet(page)
    #print('\n\n\n{}: {}'.format(query, magnet))

st = time.time()
p.make_url_list()
distros = ['archlinux', 'ubuntu', 'debian']
loop = asyncio.get_event_loop()
f = asyncio.wait([print_magnet(ur) for ur in p.make_url_list()])
loop.run_until_complete(f)
print (time.time() - st)