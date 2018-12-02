# -*- coding: utf-8 -*-

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords


def search_link(brand_name: int, product_name: int) -> str:
    df = pd.read_csv('lipstick.csv')
    df = df.drop(['Unnamed: 0'],axis = 1)
    df = df.fillna(value=str(0))
    search_df = df[(df['product_name'] == product_name) & (df['brand_name'] == brand_name)]
    link = search_df['link'].iloc[0]
    return link

def get_wordcloud(reviews):
    texts = []
    [texts.append(review) for review in reviews]
    text_string = ''
    text_string_2 = ''

    #Remove unwanted words
    DELETE_WORDS = ['lipstick', 'lip', 'idea', 'product', 'the','think', 'found','feel', 'lunch','even', 'really']
    def remove_words(text_string,DELETE_WORDS=DELETE_WORDS):
        for word in DELETE_WORDS:
            text_string = text_string.replace(word,' ')
        return text_string

    #Remove short words
    MIN_LENGTH = 1
    def remove_short_words(text_string,min_length = MIN_LENGTH):
        word_list = text_string.split()
        for word in word_list:
            if len(word) < min_length:
                text_string = text_string.replace(' '+word+' ',' ',1)
        return text_string



    for i in texts:
        string = remove_words(i)
        string = remove_short_words(string)
        text_string = text_string + string
    words = word_tokenize(text_string)
    text_string = [word.lower() for word in words
                      if word not in stopwords.words() and word.isalpha()]

    text_string_ = ''
    for i in text_string:
        text_attr = [i]
        tag = nltk.pos_tag(text_attr)
        if 'RB' in tag[0][1] or 'NN' in tag[0][1] or 'JJ' in tag[0][1]:
            text_string_ = text_string_ + ' ' + i
    bg_pic = imread('lip.jpg')
    
    wordcloud = WordCloud(stopwords=STOPWORDS,mask=bg_pic, background_color='white',width=1200,height=1500,max_words = 50).generate(text_string_)
    name = 'word_cloud.jpg'
    image_colors = ImageColorGenerator(bg_pic)

    WordCloud.to_file(wordcloud,name)