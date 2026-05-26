import pandas as pd
from collections import Counter
from kiwipiepy import Kiwi
import matplotlib.pyplot as plt

def set_font():
    plt.rc('font', family='NanumGothic')

def run_analysis(df, column_name):
    if df is None or column_name not in df.columns:
        return None
    
    raw_data = df[column_name].dropna().astype(str).tolist()
    combined_text = " ".join(raw_data)
    
    if not combined_text.strip():
        return None
    
    kiwi = Kiwi()
    tokens = []
    analysis_results = kiwi.analyze(combined_text)
    
    for result in analysis_results:
        for token in result[0]:
            tokens.append(token.form)
            
    if not tokens:
        return None
    
    token_counts = Counter(tokens)
    result_dataframe = pd.DataFrame(token_counts.most_common(20), columns=['Word', 'Score'])
    
    return result_dataframe