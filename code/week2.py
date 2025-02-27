import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
from datetime import datetime

user_agent = UserAgent()
user_agent.random

category_url = 'https://tw.news.yahoo.com/esports'
# req = requests.get( category_url )
req = requests.get(category_url, headers={ 'user-agent': user_agent.random }, timeout=5)
# 檢查請求的狀態碼
#print(req.status_code)

#print(req.text)


#print(page.prettify)
#<ul class="H(100%) Mt(10px) Pos(r) Fz(16px)">
# 解析 HTML 內容
soup = BeautifulSoup(req.text, 'html.parser')

# 找到具有特定 class 名稱的 ul 元素
ul_element = soup.find('ul', {'class': 'My(0) P(0) Wow(bw) Ov(h)'})

# 顯示找到的 ul 元素
#print(ul_element)

#items = soup.find('ul', {'class': 'My(0) P(0) Wow(bw) Ov(h)'}).findAll('li')
#print(items)


# 擷取 ul 元素中的所有 li 元素
if ul_element is None:
    print("找不到 ul 標籤，可能是 class 名稱錯誤或網頁結構改變")
    print(soup.prettify())  # 印出 HTML 原始碼，方便手動檢查
else:
    li_elements = ul_element.find_all('li')
    #print(li_elements)


news_items = soup.find_all('li', class_='stream-item')
#print(news_items)
# 存放新聞資料
news_list = []

# 遍歷每個新聞項目
for item in news_items:
    # 找標題 h3
    title_tag = item.find('h3', {'data-test-locator': 'stream-item-title'})
    # 找超連結 a
    link_tag = item.find('a', href=True)

    if title_tag and link_tag:
        title = title_tag.text.strip()
        link = link_tag['href']

        # 處理相對連結 (補上 Yahoo 網址)
        if link.startswith('/'):
            link = f"https://tw.news.yahoo.com{link}"

        # 加入新聞列表
        news_list.append({'標題': title, '連結': link})

# 顯示新聞列表
for news in news_list:
    print(f"標題: {news['標題']}")
    print(f"連結: {news['連結']}")
    print()



