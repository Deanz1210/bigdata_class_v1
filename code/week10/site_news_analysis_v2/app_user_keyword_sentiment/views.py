from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import requests
from app_user_keyword.views import filter_dataFrame
import app_user_keyword.views as userkeyword_views

#跟別人借df
# (1) Load news data--approach 1 直接指定某個csv檔案
def load_df_data_v1():
    global df # global variable
    # df = pd.read_csv('app_user_keyword/dataset/cna_news_200_preprocessed.csv',sep='|')
    df = pd.read_csv('app_user_keyword_sentiment\dataset\cna_news_e_preprocessed.csv',sep='|')

# (2) Load news data--approach 2 跟隔壁的app借用df
# import from app_user_keyword.views and use df later
def load_df_data():
    # import and use df from app_user_keyword 
    global df # global variable
    df = userkeyword_views.df

# call load data function when starting server
load_df_data_v1()
#load_df_data()


def home(request):
    return render(request, 'app_user_keyword_sentiment/home.html')

# GET: csrf_exempt is not necessary
# POST: csrf_exempt should be used
@csrf_exempt
def api_get_userkey_sentiment_from_remote_api_through_backend(request):

    userkey = request.POST['userkey']
    cate = request.POST['cate']
    cond = request.POST['cond']
    weeks = int(request.POST['weeks'])

    try:
        # (可選擇)展示從後端呼叫API: Call internet sentiment API using requests  但是不能自己呼叫自己!
        url_api_get_sentiment = "http://163.18.23.20:8000/userkeyword_senti/api_get_userkey_sentiment/"
        # Setup data for sentiment analysis request
        sentiment_data = {
            'userkey': userkey,
            'cate': cate,
            'cond': cond,
            'weeks': weeks
        }
        # Alternative way to call the sentiment API directly with requests
        sentiment_response = requests.post(url_api_get_sentiment, data=sentiment_data, timeout=5)
        if sentiment_response.status_code == 200:
            print("由後端呼叫他處API，取得情感分析數據成功!")
            # 解析來自API的回應內容。 .json() 方法會將回應的 JSON 格式資料轉換成 Python 的字典(dictionary)或列表(list)。
            # Parse the response content from the API. The .json() method converts the JSON formatted data from the response into a Python dictionary or list.
            response = sentiment_response.json()
            return JsonResponse(response)
        else:
            print(f"回傳有錯誤，進行本地處理資料")
            print(f"Sentiment API error: {sentiment_response.status_code}")
            return JsonResponse({'error': 'Failed to get sentiment analysis.'})
    except Exception as e:
        # Catch any other unexpected errors during the process
        print(f"An unexpected error occurred while processing sentiment data: {e}")
        print(f"呼叫異常失敗，進行本地處理資料")
        return JsonResponse({'error': 'An internal error occurred while processing sentiment data.'}, status=500) # Internal Server Error
 
# GET: csrf_exempt is not necessary
# POST: csrf_exempt should be used
@csrf_exempt
def api_get_userkey_sentiment(request):

    userkey = request.POST['userkey']
    cate = request.POST['cate']
    cond = request.POST['cond']
    weeks = int(request.POST['weeks'])
 
    # 進行本地處理資料
    query_keywords = userkey.split()
    # Proceed filtering
    df_query = filter_dataFrame(query_keywords, cond, cate, weeks)
    
    # if df_query is empty, return an error message
    if len(df_query) == 0:
        return JsonResponse({'error': 'No results found for the given keywords.'})
    
    sentiCount, sentiPercnt = get_article_sentiment(df_query)

    if weeks <= 4:
        freq_type = 'D'
    else:
        freq_type = 'W'

    line_data_pos = get_daily_basis_sentiment_count(df_query, sentiment_type='pos', freq_type=freq_type)
    line_data_neg = get_daily_basis_sentiment_count(df_query, sentiment_type='neg', freq_type=freq_type)

    response = {
        'sentiCount': sentiCount,
        'data_pos':line_data_pos,
        'data_neg':line_data_neg,
    }
    return JsonResponse(response)

def get_article_sentiment(df_query):
    sentiCount = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    sentiPercnt = {'Positive': 0, 'Negative': 0, 'Neutral': 0}

    df_valid = df_query.copy()

    # 將 '暫無' 替換為 0.5（中立），其他皆轉為數值
    df_valid['sentiment'] = df_valid['sentiment'].astype(str).replace('暫無', '0.5')
    df_valid['sentiment'] = pd.to_numeric(df_valid['sentiment'], errors='coerce')
    df_valid = df_valid.dropna(subset=['sentiment'])

    numberOfArticle = len(df_valid)

    for senti in df_valid['sentiment']:
        if senti >= 0.6:
            sentiCount['Positive'] += 1
        elif senti <= 0.4:
            sentiCount['Negative'] += 1
        else:
            sentiCount['Neutral'] += 1

    for polar in sentiCount:
        try:
            sentiPercnt[polar] = int(sentiCount[polar] / numberOfArticle * 100)
        except ZeroDivisionError:
            sentiPercnt[polar] = 0

    return sentiCount, sentiPercnt



def get_daily_basis_sentiment_count(df_query, sentiment_type='pos', freq_type='D'):
    df_valid = df_query.copy()

    # 同樣先將 sentiment 處理為數值
    df_valid['sentiment'] = df_valid['sentiment'].astype(str).replace('暫無', '0.5')
    df_valid['sentiment'] = pd.to_numeric(df_valid['sentiment'], errors='coerce')
    df_valid = df_valid.dropna(subset=['sentiment'])

    if sentiment_type == 'pos':
        lambda_function = lambda senti: 1 if senti >= 0.6 else 0
    elif sentiment_type == 'neg':
        lambda_function = lambda senti: 1 if senti <= 0.4 else 0
    elif sentiment_type == 'neutral':
        lambda_function = lambda senti: 1 if 0.4 < senti < 0.6 else 0
    else:
        return None

    freq_df = pd.DataFrame({
        'date_index': pd.to_datetime(df_valid['date']),
        'frequency': [lambda_function(senti) for senti in df_valid['sentiment']]
    })

    freq_df_group = freq_df.groupby(pd.Grouper(key='date_index', freq=freq_type)).sum()
    freq_df_group.reset_index(inplace=True)

    xy_line_data = [
        {'x': date.strftime('%Y-%m-%d'), 'y': freq}
        for date, freq in zip(freq_df_group['date_index'], freq_df_group['frequency'])
    ]

    return xy_line_data



print("原始 df 筆數:", len(df))
print("app_userkey_sentiment was loaded!")
