import requests
import re
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime, timedelta
from fake_useragent import UserAgent

news_links =['game-news', 'game-tips', 'esports']
news_categories=['遊戲新聞','遊戲攻略','電競賽事']
base_url = 'https://tw.news.yahoo.com/'

user_agent = UserAgent()
user_agent.random

# 存放資料之變數
links = []
titles = []
dates = []
contents = []
categories = []
item_id = []
photo_links = []

# 這裡我們需要用for迴圈爬取11個類別
# Here we need to crawl 11 categories using for loop
for i, url_short_name in enumerate(news_links):  #針對每一類 共有11類

    category = news_categories[i]  #類別名稱紀錄起來 

    # Categorical url link
    category_url = base_url + url_short_name 
    print("Getting categorical news:", category)
    print(category_url)
    # Request the categorical news page
    # req = requests.get(category_url)
    req = requests.get(category_url, headers={ 'user-agent': user_agent.random }, timeout=5)
    page = BeautifulSoup(req.text, 'html.parser')

    # 抓新聞列表
    items = page.find_all('li', class_='stream-item')
    #print(items)


    # Let's start to crawl the news in the first page for that category
    serial_no = 1
    for item_j, item in enumerate(items,start=1): #針對每一篇項目 抓其細節
        title = item.find('h3').text
        print(serial_no,'--', title )
        
        link = item.find('a').get('href')
        link = "https://tw.news.yahoo.com"+link
        print(link)

        # 儲存圖片網址變數
        image_url = None

# **方法 1: 嘗試直接抓取 <figure> 內的 <img>**
        figure_tag = page.find("figure", class_="caas-figure")
        if figure_tag:
            img_tag = figure_tag.find("img")
            if img_tag:
                image_url = img_tag.get("src") or img_tag.get("data-src")  # 優先抓 src，若無則抓 data-src


# **Yahoo 可能返回錯誤的圖片網址 (包含兩個 URL)，需要修正**
        if image_url and "https://s.yimg.com/ny/api/res/" in image_url:
            match = re.search(r'(https://s\.yimg\.com/os/creatr-uploaded-images/[\w./-]+)', image_url)
            if match:
                image_url = match.group(0)

        
       
      
        #print(f'發布於:'+news_date)
        categories.append(category)
        titles.append(title)
        links.append(link)
        #photo_links.append(image_url)
        
        
        req = requests.get(link, headers={ 'user-agent': user_agent.random }, timeout=5)
        
        page = BeautifulSoup(req.text,'html.parser')
        time_element = page.find('time', {'class': "caas-attr-meta-time"})

        if time_element:
            news_time_iso = time_element['datetime']  # 擷取 ISO 8601 格式，如："2025-02-26T07:12:09.000Z"

            news_time = datetime.strptime(news_time_iso, "%Y-%m-%dT%H:%M:%S.%fZ")

    # 轉換格式
            dtime = news_time.strftime("%Y/%m/%d %H:%M")  # 轉換為 "YYYY/MM/DD HH:MM" 格式
            news_date = news_time.strftime("%Y-%m-%d")  # 轉換為 "YYYY-MM-DD" 格式
        else:
            dtime = "未知"
            news_date = "未知"
        print(f"發布日期"+news_date)
        dates.append(news_date)
        
        # 儲存圖片網址變數
        image_url = None

# **方法 1: 嘗試直接抓取 <figure> 內的 <img>**
        figure_tag = page.find("figure", class_="caas-figure")
        if figure_tag:
            img_tag = figure_tag.find("img")
            if img_tag:
                image_url = img_tag.get("src") or img_tag.get("data-src")  # 優先抓 src，若無則抓 data-src


# **Yahoo 可能返回錯誤的圖片網址 (包含兩個 URL)，需要修正**
        if image_url and "https://s.yimg.com/ny/api/res/" in image_url:
            match = re.search(r'(https://s\.yimg\.com/os/creatr-uploaded-images/[\w./-]+)', image_url)
            if match:
                image_url = match.group(0)
        photo_links.append(image_url)
                
        item_id.append(url_short_name + "_" + news_date + "_" + str(serial_no))
        serial_no += 1
        # Find content
        content = [p.text.strip() for p in page.select(".caas-body p")]
        filtered_news = [item for item in content if not item.startswith("相關新聞")]
       
        contents.append(filtered_news)
        
        if item_j >= 4: # Here we crawl only 4 pieces of news for each category, in order to save time.
            break 
        
        #time.sleep(10)  # 遵守爬蟲禮節，請小睡一下

        
data = zip(item_id, dates, categories, titles, contents, links, photo_links)
df = pd.DataFrame(list(data), columns=['item_id','date','category','title','content','link','photo_link'])
df.head(2)
df.shape
df.content[0]
df.to_csv("cna_category_news.csv", sep="|", index=False)