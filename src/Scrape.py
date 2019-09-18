from bs4 import BeautifulSoup
import requests
import re

class Scraper:
    
    def __init__(self, url):
        self.url = url

    def scrape(self):
        
        result = self.url.find('www.amazon.in')

        if(result == -1):
            return 'Not an Amazon link 🔥'
        else:
            page = requests.get(self.url)
            
            soup = BeautifulSoup(page.text, 'html.parser')
            price = soup.find('span', {'id' : 'priceblock_dealprice'}).text
            return price


        
obj = Scraper('https://www.amazon.in/Samsung-Galaxy-Black-Storage-Offers/dp/B0756ZBZ5P/ref=sr_1_1?_encoding=UTF8&pf_rd_i=desktop&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=4430387b-ce1c-4c49-88fd-905b258011de&pf_rd_r=VFE3XHG96C1QDF7A500J&pf_rd_t=36701&qid=1565513852&s=gateway&smid=A1EWEIV3F4B24B&sr=8-1')
print(obj.scrape())
    


