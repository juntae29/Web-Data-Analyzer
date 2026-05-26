import pandas as pd
import re
import os
import matplotlib.font_manager as fm
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

def tokenize(text):
    return re.findall(r'[가-힣a-zA-Z]+', str(text))

def process_advanced_mining(df, column_name):
    data = df[column_name].dropna().astype(str)
    if data.empty: return pd.DataFrame(), {}
    
    vectorizer = TfidfVectorizer(tokenizer=tokenize, token_pattern=None, ngram_range=(1, 2), max_features=50)
    tfidf_matrix = vectorizer.fit_transform(data)
    
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    word_df = pd.DataFrame({'Word': feature_names, 'Count': scores}).sort_values(by='Count', ascending=False)
    return word_df, dict(zip(word_df['Word'], word_df['Count']))

def generate_wordcloud_obj(word_dict):
    # 폰트 경로를 프로젝트 루트에서 직접 지정
    font_path = os.path.join(os.getcwd(), "NanumGothic.ttf")
    
    # 폰트 파일 존재 여부 확인 후 로드
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