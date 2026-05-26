import pandas as pd
import re
import os
import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud

def get_font():
    font_path = "/tmp/NanumGothic.ttf"
    if not os.path.exists(font_path):
        try:
            url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
            response = requests.get(url, timeout=10)
            with open(font_path, "wb") as f:
                f.write(response.content)
        except: return None
    return font_path

def tokenize(text):
    return re.findall(r'[가-힣a-zA-Z]+', str(text))

def process_kh_analysis(df, column_name):
    data = df[column_name].dropna().astype(str)
    if data.empty: return None, None, None
    
    vectorizer = TfidfVectorizer(tokenizer=tokenize, token_pattern=None, min_df=2)
    tfidf = vectorizer.fit_transform(data)
    words = vectorizer.get_feature_names_out()
    
    # 단어 간 공기 관계 (Similarity Matrix)
    sim_matrix = cosine_similarity(tfidf.T)
    word_freq = dict(zip(words, tfidf.sum(axis=0).A1))
    
    return words, sim_matrix, word_freq

def generate_wordcloud_obj(word_dict):
    wc = WordCloud(width=800, height=400, background_color='white', font_path=get_font())
    return wc.generate_from_frequencies(word_dict) if word_dict else wc