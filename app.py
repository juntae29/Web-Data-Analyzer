import streamlit as st
import pandas as pd
from analyzer import process_advanced_mining, generate_wordcloud_obj, map_taxonomy

st.set_page_config(layout="wide")
st.title("Data Mining Analyzer (KH Coder Integrated)")

# 사이드바 입력
mode = st.sidebar.radio("Source", ["CSV", "Text"])
df = None
if mode == "CSV":
    f = st.file_uploader("Upload", type=["csv"])
    if f: df = pd.read_csv(f)
else:
    t = st.text_area("Input Text")
    if t: df = pd.DataFrame({"Content": [t]})

if df is not None:
    col = st.selectbox("Column", df.columns)
    cat_name = st.text_input("Category", "Methodology")
    cat_words = st.text_input("Keywords", "분석, 모델, 데이터")
    
    if st.button("Run Analysis"):
        word_df, word_dict, corr_df = process_advanced_mining(df, col)
        
        t1, t2, t3 = st.tabs(["Dashboard", "Taxonomy", "Co-occurrence Network"])
        with t1:
            st.image(generate_wordcloud_obj(word_dict).to_array())
        with t2:
            st.table(map_taxonomy(word_df, {cat_name: cat_words})[cat_name])
        with t3:
            st.write("단어 간 관계 (유사도 행렬)")
            st.dataframe(corr_df.style.background_gradient(cmap='Blues'))