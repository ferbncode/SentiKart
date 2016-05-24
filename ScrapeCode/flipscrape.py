import math
from mydict import MyDict
import asyncio
import aiohttp
import bs4
import tqdm
import re

class Product():
    def __init__(self,url,revc=30):
        self.url = url
        self.pname = self.url.split('/')
        self.pname = self.pname[3]
        self.image = self.get_image()
        self.revc = revc
        self.revp = int(self.revc/10+1)
        self.url = re.sub(r'/p/', r'/product-reviews/', self.url)
        self.url +='&rating=1,2,3,4,5&reviewers=all&type=all&sort=most_helpful&start='
        print(self.url)

    def get_image(self):
        
    def make_url_list(self):
        lis = []
        for i in range(self.revp):
            url = self.url
            url += str(i*10)
            lis.append(url)
        return lis

    # @asyncio.coroutine
    # def get_url(url):
    #     wait_time = random.randint(1, 4)
    #     #yield from asyncio.sleep(wait_time)
    #     print('Done: URL {} took {}s to get!'.format(url, wait_time))
    #     resp = requests.get(url)
    #     body = resp.text
    #     return len(body)
    
        
#@app.route('/')
def hell():
    loop = asyncio.get_event_loop()
    print("First, process results as they come in:")
    loop.run_until_complete(process_once_everything_ready())


#if __name__ == '__main__':
#    set_url()
#    hell()  
    #make_url_list()