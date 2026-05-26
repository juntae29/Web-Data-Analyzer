import pandas as pd
from collections import Counter
from kiwipiepy import Kiwi
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def set_font():
    plt.rc('font', family='NanumGothic')

def run_analysis(df, column_name):
    if df is None or column_name not in df.columns:
        return None, None
    
    # 텍스트 데이터 추출 및 정제
    raw_data = df[column_name].dropna().astype(str).tolist()
    combined_text = " ".join(raw_data)
    
    if not combined_text.strip():
        return None, None
    
    kiwi = Kiwi()
    tokens = []
    # 한국어 형태소 분석
    analysis_results = kiwi.analyze(combined_text)
    
    for result in analysis_results:
        for token in result[0]:
            tokens.append(token.form)
            
    if not tokens:
        return None, None
    
    token_counts = Counter(tokens)
    # 통계적 관점에서 Frequency로 컬럼명 지정
    result_dataframe = pd.DataFrame(token_counts.most_common(20), columns=['Word', 'Frequency'])
    
    return result_dataframe, token_counts

def generate_wordcloud(token_counts):
    # 환경에 따라 폰트 경로 확인 필요
    wc = WordCloud(
        font_path='/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
        background_color='white',
        width=800, height=400
    ).generate_from_frequencies(dict(token_counts))
    return wc