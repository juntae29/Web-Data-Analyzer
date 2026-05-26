import pandas as pd
import re
import os
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

# 1. 폰트 다운로드 (서버 안전성 확보)
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

# 2. 한글 형태소 분석기 대체 (정규식 기반 토큰화)
def tokenize(text):
    # 한글 어절 및 영문 단어 추출
    return re.findall(r'[가-힣a-zA-Z]+', str(text))

# 3. 데이터 분석 엔진
def process_advanced_mining(df, column_name):
    data = df[column_name].dropna().astype(str)
    if data.empty: return pd.DataFrame(), {}
    
    vectorizer = TfidfVectorizer(tokenizer=tokenize, token_pattern=None, ngram_range=(1, 2), max_features=100)
    tfidf_matrix = vectorizer.fit_transform(data)
    
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    word_df = pd.DataFrame({'Word': feature_names, 'Score': scores}).sort_values(by='Score', ascending=False)
    return word_df, dict(zip(word_df['Word'], word_df['Score']))

# 4. 워드클라우드 및 매핑
def generate_wordcloud_obj(word_dict):
    wc = WordCloud(width=800, height=400, background_color='white', font_path=get_font())
    return wc.generate_from_frequencies(word_dict) if word_dict else wc

def map_taxonomy(word_df, taxonomy_dict):
    results = {}
    for category, keywords in taxonomy_dict.items():
        targets = [k.strip() for k in keywords.split(",")]
        results[category] = word_df[word_df['Word'].isin(targets)]
    return results