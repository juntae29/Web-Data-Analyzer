import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
import matplotlib.pyplot as plt

def set_font():
    plt.rc('font', family='NanumGothic')

def tokenizer(text):
    okt = Okt()
    return okt.nouns(text)

def run_analysis(df, column_name):
    if df is None or column_name not in df.columns:
        return None, None, None, None
    
    data = df[column_name].dropna().astype(str).tolist()
    
    if not data or all(len(d.strip()) == 0 for d in data):
        return None, None, None, None
    
    vectorizer = TfidfVectorizer(tokenizer=tokenizer, token_pattern=None, max_features=1000)
    
    try:
        tfidf = vectorizer.fit_transform(data)
    except ValueError:
        return None, None, None, None
    
    word_freq = pd.Series(tfidf.sum(axis=0).A1, index=vectorizer.get_feature_names_out())
    result_df = word_freq.reset_index().rename(columns={'index': 'Word', 0: 'Score'})
    
    return word_freq.to_dict(), None, result_df, None