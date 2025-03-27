import pandas as pd
import ast
import json  # Import json to parse data safely
from collections import Counter

# Load DataFrame
df = pd.read_csv("D:\\project_code\\bigdata_class_v1\\030\\cna_news_preprocessed.csv", sep='|')


def NerToken(word, ner, idx):
    # print(ner, word)
    return ner, word

# Allowed named entity types
allowedNE = ['PERSON']
news_categories = ['PC','動漫畫','電競','活動展覽']
filtered_words =[]
for ner,word in eval(df.entities[0]):
    if (len(word) >= 2) & (ner in allowedNE):
        filtered_words.append(word)

#print(filtered_words)

counter = Counter( filtered_words )
counter.most_common( 200 )

def ne_word_frequency( a_news_ne ):
    filtered_words =[]
    for ner,word in a_news_ne:
        if (len(word) >= 2) & (ner in allowedNE):
            filtered_words.append(word)
    counter = Counter( filtered_words )
    return counter.most_common( 200 )

def get_top_ner_words():
    top_cate_ner_words={}
    words_all=[]
    for category in news_categories:
        df_group = df[df.category == category]
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
    #return top_cate_ne_words

hotPersons = get_top_ner_words()

df_hotPersons = pd.DataFrame(hotPersons, columns = ['category','top_keys'])
print("Saving to file...")
df_hotPersons.to_csv('D:\\project_code\\bigdata_class_v1\\030\\news_top_person_by_category_via_ner.csv', sep=',', index=False)
print("File saved successfully.")


