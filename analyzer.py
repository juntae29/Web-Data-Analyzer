import pandas as pd
import re
import os
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud

# 1. 폰트 관리
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

# 2. 형태소 분석기 복구 (정규식 기반)
def tokenize(text):
    return re.findall(r'[가-힣a-zA-Z]+', str(text))

# 3. 기존 분석 + KH Coder 스타일의 정량적 분석 통합
def process_advanced_mining(df, column_name):
    data = df[column_name].dropna().astype(str)
    if data.empty: return pd.DataFrame(), {}, None
    
    vectorizer = TfidfVectorizer(tokenizer=tokenize, token_pattern=None, ngram_range=(1, 2), max_features=100)
    tfidf = vectorizer.fit_transform(data)
    
    # 단어 빈도 데이터
    words = vectorizer.get_feature_names_out()
    scores = tfidf.sum(axis=0).A1
    word_df = pd.DataFrame({'Word': words, 'Score': scores}).sort_values(by='Score', ascending=False)
    
    # 공기 관계(Co-occurrence) 분석을 위한 유사도 행렬
    sim_matrix = cosine_similarity(tfidf.T)
    corr_df = pd.DataFrame(sim_matrix, index=words, columns=words)
    
    return word_df, dict(zip(words, scores)), corr_df

# 4. 기능 유지
def generate_wordcloud_obj(word_dict):
    wc = WordCloud(width=800, height=400, background_color='white', font_path=get_font())
    return wc.generate_from_frequencies(word_dict) if word_dict else wc

def map_taxonomy(word_df, taxonomy_dict):
    results = {}
    for category, keywords in taxonomy_dict.items():
        targets = [k.strip() for k in keywords.split(",")]
        results[category] = word_df[word_df['Word'].isin(targets)]
    return results