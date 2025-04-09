from django.shortcuts import render 
from django.http import JsonResponse 
import pandas as pd  
from django.views.decorators.csrf import csrf_exempt

# 渲染首頁
def home(request): 
    return render(request, 'app_word_cloud/home.html') 

# 讀取資料
df_topkey = pd.read_csv('app_word_cloud/dataset/cna_news_topkey_with_category_via_token_pos.csv', sep=',') 

# 整理成字典
data = {}
for idx, row in df_topkey.iterrows(): 
    data[row['category']] = eval(row['top_keys']) 

del df_topkey

@csrf_exempt
def api_get_cate_topword(request): 
    cate = request.POST.get('news_category') 
    topk = int(request.POST.get('topk')) 

    chart_data, wf_pairs = get_category_topword(cate, topk)

    response = {
        'chart_data': chart_data,
        'wf_pairs': wf_pairs,
    }

    return JsonResponse(response)

def get_category_topword(cate, topk=10): 
    if cate == "全部":
        # 整合所有類別的詞頻資料
        combined = []
        for cat in data:
            combined.extend(data[cat])
        
        # 統計詞頻
        freq_dict = {}
        for word, freq in combined:
            freq_dict[word] = freq_dict.get(word, 0) + freq

        # 轉成 list 並排序
        sorted_pairs = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
        wf_pairs = sorted_pairs[:topk]
    else:
        wf_pairs = data.get(cate, [])[:topk]

    words = [w for w, f in wf_pairs]
    freqs = [f for w, f in wf_pairs]

    chart_data = {
        "category": cate,
        "labels": words,
        "values": freqs
    }

    return chart_data, wf_pairs

print("app_word_cloud--類別熱門關鍵字載入成功!")
