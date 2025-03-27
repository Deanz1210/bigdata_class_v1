import pandas as pd
from collections import Counter
import pandas as pd
from datetime import datetime, timedelta
df = pd.read_csv('D:\\project_code\\bigdata_class_v1\\030\\cna_news_preprocessed.csv',sep='|')
## Filter news
# Appraoch 1: Filter by time duration
# end date: the date of the latest record of news
end_date = df.date.max()
# start date
start_date = (datetime.strptime(end_date, '%Y-%m-%d').date() - timedelta(days=1)).strftime('%Y-%m-%d') # 昨日誰最大
#start_date = (datetime.strptime(end_date, '%Y-%m-%d').date() - timedelta(days=7)).strftime('%Y-%m-%d') # 上週誰最大
# Filter news
query_df = df[(df.date >= start_date) & (df.date <= end_date)] 
allowedNE=['PERSON']
news_categories=['PC','動漫畫','電競','活動展覽']
def NerToken(word, ner, idx):
    # print(ner,word)
    return ner,word
def ne_word_frequency( a_news_ne ):
    filtered_words =[]
    for ner,word in a_news_ne:
        if (len(word) >= 2) & (ner in allowedNE):
            filtered_words.append(word)
    counter = Counter( filtered_words )
    return counter.most_common( 5 )
def get_top_ner_words(query_df):
    top_cate_ner_words={}
    words_all=[]
    for category in news_categories:
        df_group = query_df[query_df.category == category]
        words_group = []

        # concatenate terms in a category
        for row in df_group.entities:
            words_group += eval(row)

        # concatenate all terms
        words_all += words_group

        # Get top words by calling ne_word_frequency() function
        topwords = ne_word_frequency( words_group )
        top_cate_ner_words[category] = topwords

    topwords_all = ne_word_frequency(words_all)
    top_cate_ner_words['全部'] = topwords_all
    
    return list(top_cate_ner_words.items())
    # return top_cate_ne_words
popularPersons = get_top_ner_words(query_df)
popularPersons
df_popularPersons = pd.DataFrame(popularPersons, columns = ['category','top_keys'])
df_popularPersons
df_popularPersons.to_csv('D:\\project_code\\bigdata_class_v1\\030\\popular-persons-of-yesterday.csv', sep=',', index=False)