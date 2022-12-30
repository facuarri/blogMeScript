# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 23:32:52 2022

@author: Facu
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#reading excel file
data = pd.read_excel('articles.xlsx')

#counting number of articles per source
data.groupby(['source_id'])['article_id'].count()
data.groupby(['source_id']).size()
data.groupby(['source_id']).count()

#number of reactions by publisher
data.groupby(['source_id'])['engagement_reaction_count'].sum()

#dropping a column
data = data.drop('engagement_comment_plugin_count', axis = 1)

#creating a keywordflag function
def keywordflag(keyword):
    length = len(data)
    keyword_flag = []
    for x in range(0, length):
        try:
            if keyword in data['title'][x]:
                flag = 1
            else:
                flag = 0
        except:
            flag = 0
        keyword_flag.append(flag)
    return keyword_flag

keywordflag = keywordflag('murder')

#creating new column in dataframe
data['keyword_flag'] = pd.Series(keywordflag)

#SentimentIntensityAnalyzer

#neg = sent['neg']
#pos = sent['pos']
#neu = sent['neu']

sent_int = SentimentIntensityAnalyzer()
title_neg_sentiment = []
title_pos_sentiment = []
title_neu_sentiment = []

length = len(data)

for x in range(0, length):
    try:
        text = data['title'][x]
        sent = sent_int.polarity_scores(text)
        title_neg_sentiment.append(sent['neg'])
        title_pos_sentiment.append(sent['pos'])
        title_neu_sentiment.append(sent['neu'])
    except:
        title_neg_sentiment.append(0)
        title_pos_sentiment.append(0)
        title_neu_sentiment.append(0)
        
title_neg_sentiment = pd.Series(title_neg_sentiment)
title_pos_sentiment = pd.Series(title_pos_sentiment)
title_neu_sentiment = pd.Series(title_neu_sentiment)

data['title_neg_sentiment'] = title_neg_sentiment
data['title_pos_sentiment'] = title_pos_sentiment
data['title_neu_sentiment'] = title_neu_sentiment

#writing data to excel file
data.to_excel('blogme_clean.xlsx', sheet_name='blogmedata', index = False)