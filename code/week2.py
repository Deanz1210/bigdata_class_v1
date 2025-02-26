import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent

user_agent = UserAgent()
user_agent.random

category_url = 'https://tw.news.yahoo.com/game-3c'
# req = requests.get( category_url )
req = requests.get(category_url, headers={ 'user-agent': user_agent.random }, timeout=5)
# 檢查請求的狀態碼
#print(req.status_code)

# print(req.text)


#print(page.prettify)
#<ul class="H(100%) Mt(10px) Pos(r) Fz(16px)">
# 解析 HTML 內容
soup = BeautifulSoup(req.text, 'html.parser')

# 找到具有特定 class 名稱的 ul 元素
ul_element = soup.find('ul', {'class': 'H(100%) Mt(10px) Pos(r) Fz(16px)'})

# 顯示找到的 ul 元素
#print(ul_element)

#items = soup.find('ul', {'class': 'H(100%) Mt(10px) Pos(r) Fz(16px)'}).findAll('li')
#print(items)


# 擷取 ul 元素中的所有 li 元素
li_elements = ul_element.find_all('li')

#print(li_elements)

# 遍歷每個 li 元素，擷取新聞標題和連結
"""
# 存放新聞資料
news_list = []

# 遍歷每個 li 元素，擷取新聞標題和連結
for li in li_elements:
    # 找到 a 標籤
    a_tag = li.find('a')
    
    if a_tag:
        title = a_tag.text.strip()
        link = a_tag['href']
        
        # 處理相對連結
        if link.startswith('/'):
            link = f"https://tw.news.yahoo.com{link}"
        
        # 將新聞資料添加到列表中
        news_list.append({'標題': title, '連結': link})

# 顯示新聞列表
for news in news_list:
    print(f"標題: {news['標題']}")
    print(f"連結: {news['連結']}")
    print()
"""
#找標題
"""
items = soup.find('ul', {'class': 'H(100%) Mt(10px) Pos(r) Fz(16px)'}).findAll('li')
item = items[0]
a_tag = item.find('a')
if a_tag:
    title = a_tag.text.strip()
    print(f"標題: {title}")
else:
    print("未找到標題")
"""
