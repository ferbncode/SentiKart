import sqlite3
import requests
import nltk
import time
import datetime
import re
from bs4 import BeautifulSoup

# proxy
http_proxy = "http://172.16.24.2:3128"
ftp_proxy = "ftp://172.16.24.2:3128"
https_proxy = "https://172.16.24.2:3128"

proxyDict = {
                "http" : http_proxy,
                "https" : https_proxy,
                "ftp" : ftp_proxy
            }


# link database
link_list = []

# database stuff
conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()

def comprehend(text):
    tokenized = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokenized)
    nameE = nltk.ne_chunk(tagged, binary = True)
    entities =  re.findall(r'NE\s(.*?)/', str(nameE))
    descriptives = re.findall(r"\n\s\s(\w+)/JJ", str(nameE))
    #print "Enitites: ", entities
    #print "Descriptives: ", descriptives

    # limiting ourselves with just one entity per paragraph
    if len(entities) == 0:
        return
    entities = entities[0]
    print 'Entities:', entities
    for eachD in descriptives:
        print 'Description:', eachD
        currentTime = time.time()
        dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%d-%m-%y %h:%m:%s')
        relatedWord = eachD
        c.execute("""insert into Knowledgebase (unix, dateStamp, entities, relatedWord) values (?,?,?,?)""", (currentTime, dateStamp, entities, relatedWord))
        conn.commit()
    print '\n'


def LoadSoup(link):
    try:
        r = requests.get(link, proxies='proxyDict')
    # try again if there is some error
    except Exception, e:
        print 'Error in geting response: ', e
        LoadSoup(link)
    soup = BeautifulSoup(r.text)
    if soup.title.text == 'Resource Not Found':
        print soup.title.text
        return 0
    return soup

def TOIRSS():
    try:
        #RSSlink = "http://timesofindia.indiatimes.com/rssfeeds/5880659.cms"
        RSSlink = "http://feeds.huffingtonpost.com/huffingtonpost/raw_feed"

        print 'Working fine till here'
        time.sleep(555)

        soup = LoadSoup(RSSlink)
        # finding titles in the soup
        titles = []
        titles = [title.text for title in soup.find_all('title')]
        # first titles is of no use
        # for times of india feed, this offset is 2 instead of 1

        titles = titles[1:]

        # finding links in the soup
        links = []
        links = [link.text for link in soup.find_all('guid')]

        # some neat exception handling
        if len(links) != len(titles):
            print "Number of links and titles mismatch"
            return

        print 'Working fine till here'
        time.sleep(555)
        # printing the titles
        for i in range(len(titles)):
            print i+1, "\b)", titles[i]

        # printing the links
        #for i in range(len(links)):
            #print i+1,"\b)", links[i]

        # visiting articles
        for i in range(len(links)):
            if links[i] in link_list:
                print 'link already scraped'
            else:
                link_list.append(links[i])
                print "Going to link: ", links[i]
                soupage = LoadSoup(links[i])
                print 'Aloo Pyaj'
                for content in soupage.find_all('p'):
                    comprehend(content.text.strip())

    except Exception, e:
        print e


while True:
    TOIRSS()
    time.sleep(600)
comprehend('Utkarsh is so cool and totally amazing but Shikhar has got some real stuff up there.')

