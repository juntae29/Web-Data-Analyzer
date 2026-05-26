import pandas as pd
import re
import os
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

# 한글 폰트가 없는 환경을 위해 폰트 설정 강제화
def generate_wordcloud_obj(word_dict):
    # 폰트 경로를 명시하지 않고, 폰트 파일이 로컬에 있으면 사용, 없으면 영문 전용으로 작동하게 함
    font_path = "NanumGothic.ttf"
    
    # 폰트 파일이 실제 존재하는지 확인
    if not os.path.exists(font_path):
        font_path = None
        
    wc = WordCloud(
        width=800, height=400, 
        background_color='white', 
        font_path=font_path
    )
    
    if not word_dict: return wc
    wc.generate_from_frequencies(word_dict)
    return wc

# 기존 토큰화 및 분석 로직
def tokenize(text):
    return re.findall(r'[가-힣a-zA-Z]+', str(text))

def process_advanced_mining(df, column_name):
    data = df[column_name].dropna().astype(str)
    if data.empty: return pd.DataFrame(), {}
    vectorizer = TfidfVectorizer(tokenizer=tokenize, token_pattern=None, ngram_range=(1, 2), max_features=50)
    tfidf_matrix = vectorizer.fit_transform(data)
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    return pd.DataFrame({'Word': feature_names, 'Count': scores}).sort_values(by='Count', ascending=False), dict(zip(feature_names, scores))

def map_taxonomy(word_list, taxonomy_dict):
    results = {}
    for category, keywords in taxonomy_dict.items():
        targets = [k.strip() for k in keywords.split(",")]
        results[category] = [word for word in word_list if word in targets]
    return results