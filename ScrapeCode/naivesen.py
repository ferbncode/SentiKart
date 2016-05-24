# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:29:22 2016

@author: Utkarsh
"""

# TO-DO
# change name for linux '/' instead of '\' in windows


#   TEST RESULTS 
#   Since file was loaded from file, it should be much faster in real-time
#   ResultS
#   [1, -4699.969402707354, -4790.978339475781]

#t[b]
#Out[437]: [0, -4057.3610046455115, -3968.6529978376]
import math
from mydict import MyDict
import asyncio
import aiohttp
import bs4
import tqdm
import re

try:
    with open('stopwords.txt','r') as f:
        stopwords = set(f.readline().split())
except:
    print(os.getcwd())
    print('Cannot load stopwords',e)

def get_features(text):
    features = []
    negated = False
    clean_text = re.sub(r'[^a-zA-Z0-9\']', ' ', text)
    for feature in clean_text.split():
        if not feature in stopwords:
            if feature in ['not','n\'t','no']:
                negated = True
            else:
                if negated == True:
                    feature = 'not_'+feature
                    negated = False
                features.append(feature)
    return features
    
def get_features_from_file(file_name):
    f = open(file_name, encoding="utf8")
    text = f.read()
    text = text.lower()
    f.close()
    return get_features(text.strip())


                
    # @asyncio.coroutine
    # def process_once_everything_ready():
    #     coroutines = [get_url(url) for url in make_url_list()]
    #     results = yield from asyncio.gather(*coroutines)
    #     analysis = []
    # #for rev in results:
    #    soup = BeautifulSoup(rev, "lxml")
    #    dates = soup.findAll('div', {'class':'date line fk-font-small'})
    #    texts = soup.findAll('span', {'class':'review-text'})
    #    for date, txt in zip(dates, texts):
    #        analysis.append([date, get_analysis(txt)])
        #print (analysis)

#load_pickle()

class NaiveBayes():
    def __init__(self):
        import pickle
        self.pos = MyDict()
        self.neg = MyDict()
        self.tot_pos, self.pos = pickle.load(open('pos_file', 'rb'))
        self.tot_neg, self.neg = pickle.load(open('neg_file', 'rb'))
    def train(self):
        path_to_pos = '.\\aclImdb\\train\\pos\\'
        path_to_neg = '.\\aclImdb\\train\\neg\\'
        self.tot_pos = 0
        self.tot_neg = 0        
        limit = 12500
        docs_c = 0
        for file_name in os.listdir(path_to_pos)[:limit]:
            for word in get_features_from_file(path_to_pos+file_name):
                self.pos[word] += 1
                self.neg['not_'+word] += 1
                self.tot_pos += 1
                self.tot_neg += 1
            docs_c += 1
        for file_name in os.listdir(path_to_neg)[:limit]:
            for word in get_features_from_file(path_to_neg+file_name):
                self.neg[word] += 1
                self.tot_neg += 1
                self.pos['not_'+word] += 1
                self.tot_pos += 1
            docs_c += 1
        print ('DOCS On which I trained: %d' %(docs_c,))
        pickle.dump((self.tot_pos, self.pos), open('pos_file', 'wb'))
        pickle.dump((self.tot_neg, self.neg), open('neg_file', 'wb'))        
    def classify(self, text):
        pos_sent = 0
        neg_sent = 0
        features = set(get_features(text))
        for w in features:
            pos_sent += math.log((self.pos[w]+1.0)/(2.0*self.tot_pos))
            neg_sent += math.log((self.neg[w]+1.0)/(2.0*self.tot_neg))
        #return (pos_sent, neg_sent)
        return normalize_score(pos_sent, neg_sent) 
    def working(self):
        print('Working!!!!!!!')
        time.sleep(1)
        
def normalize_score(p, n):
    m = 0
    if p - n < -10:
        m = -10
    if p - n > 10:
        m  = 10
    if abs(p-n) < 4:
        m = abs(p-n) + 4
    else:
        m = p-n
    if m > 10:
        m = 10
    if m < -10:
        m = -10
    return m

if __name__ == '__main__':
    t = NaiveBayes()
    print(t.classify('i am terrible pathetic stupid bad ridiculous'))
    print(t.classify('he is smart talented hard-working cool'))
   