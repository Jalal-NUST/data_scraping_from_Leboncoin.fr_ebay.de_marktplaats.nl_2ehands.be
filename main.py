import requests,time,random,queue
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options

data_new= pd.DataFrame(columns= ['img_link','Title','Price','page_index'])
q = queue.Queue()
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 
chrome_options = Options()

############################################################
class Scrap:

    def popup(self):
        self.browser = webdriver.Chrome('chromedriver.exe', options=chrome_options)
        self.browser.get('https://ebay.de/')
        time.sleep(10)
        self.browser.find_element_by_id("gdpr-banner-accept").click()
    def search(self,search_item='Porzellan'):
        search_200 = 'https://www.ebay.de/sch/i.html?_from=R40&_nkw={s}&_sacat=0&_ipg=200'.format(s=search_item)
        self.browser.get(search_200)
    def next_page(self,page_no,search_item='Porzellan'):
        next_page ='https://www.ebay.de/sch/i.html?_from=R40&_nkw={s}&_sacat=0&_ipg=200&_pgn={p}'.format(s=search_item,p=page_no)
        self.browser.get(next_page)
    def scrap_data(self,data_new=data_new):
        src = self.browser.page_source
        soup = BeautifulSoup(src,'lxml')
        items = soup.find_all('div',{'class':"s-item__wrapper clearfix"})
        time.sleep(3)
        for item in range(200):
            dic_new={}
            title = items[item].find('h3',{'class':"s-item__title"}).get_text().strip()
            price = items[item].find('span',{'class':"s-item__price"}).get_text().strip()
            img = items[item].find('div',{'class':"s-item__image-wrapper"})
            a = [img['href'] if img.get('href') is not None else img['src'] for img in img.select('[href^="http"], [src^="http"]') ]
            link = a[0][:-5]+'.jpg'
            dic_new['img_link']= link
            dic_new['Title']= title
            dic_new['Price']= price
            q.put(dic_new)
####################################################################

s=Scrap()
s.popup()
s.search()
s.scrap_data()
count = 0
while(not(q.empty())):
    count = count + 1
    result = q.get()
#     print(count," --> " , result)
    data_new = data_new.append(result, ignore_index=True)
data_new.to_csv(r'eBay.csv')