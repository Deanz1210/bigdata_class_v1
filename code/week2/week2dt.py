import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
from datetime import datetime

user_agent = UserAgent()
user_agent.random

category_url = 'https://tw.news.yahoo.com/%E3%80%8A%E8%8B%B1%E9%9B%84%E8%81%AF%E7%9B%9F%E3%80%8Blta%E4%BB%A3%E8%A1%A8tl%E5%8F%AA%E6%89%9317%E5%A0%B4%E6%AF%94%E8%B3%BD%E5%B0%B1%E5%A5%AA%E5%86%A0%E5%BC%95%E8%AD%B0%EF%BC%8C%E7%9B%B4%E6%8E%A5%E6%AF%94%E9%9F%93%E5%9C%8Bhle%E5%B0%91%E4%BA%86%E4%B8%80%E5%8D%8A-063603609.html'
# req = requests.get( category_url )c
req = requests.get(category_url, headers={ 'user-agent': user_agent.random }, timeout=5)
#print(req.status_code)

#print(req.text)

soup = BeautifulSoup(req.text, 'html.parser')

"""
# 取得新聞時間標籤
time_element = soup.find('time', {'class': "caas-attr-meta-time"})

if time_element:
    news_time_iso = time_element['datetime']  # 擷取 ISO 8601 格式，如："2025-02-26T07:12:09.000Z"

    news_time = datetime.strptime(news_time_iso, "%Y-%m-%dT%H:%M:%S.%fZ")

    # 轉換格式
    dtime = news_time.strftime("%Y/%m/%d %H:%M")  # 轉換為 "YYYY/MM/DD HH:MM" 格式
    news_date = news_time.strftime("%Y-%m-%d")  # 轉換為 "YYYY-MM-DD" 格式
else:
    dtime = "未知"
    news_date = "未知"

# 印出結果
print(f"新聞日期: {news_date}")
"""
"""
# 儲存圖片網址變數
image_url = None

# **方法 1: 嘗試直接抓取 <figure> 內的 <img>**
figure_tag = soup.find("figure", class_="caas-figure")
if figure_tag:
    img_tag = figure_tag.find("img")
    if img_tag:
        image_url = img_tag.get("src") or img_tag.get("data-src")  # 優先抓 src，若無則抓 data-src


# **Yahoo 可能返回錯誤的圖片網址 (包含兩個 URL)，需要修正**
if image_url and "https://s.yimg.com/ny/api/res/" in image_url:
    match = re.search(r'(https://s\.yimg\.com/os/creatr-uploaded-images/[\w./-]+)', image_url)
    if match:
        image_url = match.group(0)

# **輸出最終圖片網址**
if image_url:
    print("新聞圖片網址:", image_url)
else:
    print("未找到圖片")

"""
# 擷取 `.caas-body` 內所有 <p> 標籤的內容
paragraphs = [p.text.strip() for p in soup.select(".caas-body p")]

# 過濾掉包含「相關新聞」的段落
filtered_news = [item for item in paragraphs if not item.startswith("相關新聞")]

# 重新編號並輸出
for i, text in enumerate(filtered_news, 1):
    print(f"{i}. {text}")