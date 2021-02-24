import requests,time,random,queue
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from os import system, name 

data_new= pd.DataFrame(columns= ['Title','Price','item_link'])
data_new1= pd.DataFrame(columns= ['Title','Price','Description','item_link'])
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
        self.browser.get('https://www.2dehands.be/')
        time.sleep(10)
        self.browser.find_element_by_id("gdpr-consent-banner-accept-button").click()
        
    def search(self,search_item='porselein'):
        search_200 = 'https://www.2dehands.be/q/{s}/'.format(s=search_item)
        self.browser.get(search_200)
        time.sleep(2)
    def next_page(self,page_no,search_item='porselein'):
        next_page ='https://www.2dehands.be/q/{s}/p/{p}/'.format(s=search_item,p=page_no)
        self.browser.get(next_page)
        try:
            browser.find_element_by_class_name('hz-Icon hz-Icon--m hz-SvgIcon hz-SvgIconClose').click()
        except:
            pass
        time.sleep(2)
    def scrap_data(self):
        dic_new={}
        src = self.browser.page_source
        soup = BeautifulSoup(src,'lxml')
        total_pages= soup.find('span',{'class':"mp-PaginationControls-pagination-pageList"}).find_all('span')[2].get_text()
        # print('Total ',total_pages,' pages found...')
        
        items = soup.find_all('li',{'class':"mp-Listing mp-Listing--list-item "})
        time.sleep(3)
        for item in range(len(items)):
            dic_new={}
            title = items[item].find('h3',{'class':"mp-Listing-title"}).get_text().strip()
            price = items[item].find('span',{'class':"mp-Listing-price mp-text-price-label"}).get_text().strip().replace("\xa0"," ")
            
            item_link = 'https://www.2dehands.be/'+ items[item].find('a',{'class':"mp-Listing-coverLink"})['href']
            dic_new['Title']= title
            dic_new['Price']= price
            dic_new['item_link']= item_link
            q.put(dic_new)
        return total_pages
        
            
    def open_item(self,item_link):
        self.browser.get(item_link)
        
    
            
    def scrap_img(self,item_link,item_title):
        dic_new={}
        dic_new['item_link']= item_link
        dic_new['Title']= item_title
#         dic_new['Price']= item_price
        src = self.browser.page_source
        soup = BeautifulSoup(src,'lxml')
        imgs = soup.find_all('div',{'class':"image "})
        for img in range(4):
            try:
                image = 'https:' + imgs[img].find('img')['src']
                dic_new['img_link'+str(img)]= image
            except:
                pass
        price = soup.find('span',{'class':"price "}).get_text().strip()
        des = soup.find('div',{'class':"wrapped"}).get_text().strip()  
        dic_new['Price']= price
        dic_new['Description']= des[:150]
        q.put(dic_new)


##################################################################

s=Scrap()
s.popup()
s.search()
total = s.scrap_data()
clear()
print('Total ',total,' pages found...')
pages = eval(input('How many pages to scrap data from? (excluding main search page)  '))
st_page= eval(input('From which page scraping should begin?  '))
for page in range(st_page,st_page+pages+1):
    
    s.next_page(page_no = page,search_item='porselein')
    s.scrap_data()
    time.sleep(3)


#####################################################################
count = 0
while(not(q.empty())):
    count = count + 1
    result = q.get()
#     print(count," --> " , result)
    data_new = data_new.append(result, ignore_index=True)
# data_new.to_csv(r'2dehands_init.csv'))
######################################################################
# data = pd.read_csv(r'2dehands_init.csv', encoding= 'unicode_escape'))
data = data_new
print("finish lop")
print(len(data.iloc[:,2]))
for i in range(len(data.iloc[:,2])):
    link =data.iloc[i,2]
    title =data.iloc[i,0]
#     price =data.iloc[i,2]
    s.open_item(link)
    
    s.scrap_img(link,title)
    
# count = 0
# while(not(q.empty())):
#     count = count + 1
#     result = q.get()
# #     print(count," --> " , result)
#     data_new1 = data_new1.append(result, ignore_index=True)
# data_new1.to_csv(r'final_2dehands.csv')