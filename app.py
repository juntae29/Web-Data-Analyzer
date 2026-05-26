import streamlit as st
import pandas as pd
from analyzer import process_kh_analysis, generate_wordcloud_obj

st.set_page_config(layout="wide", page_title="KH Coder Style Analyzer")
st.title("Advanced Content Analyzer (KH Coder Style)")

# 데이터 로드 로직 (생략 - 기존 방식 유지)
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    col = st.selectbox("Select Column:", df.columns)
    
    if st.button("Run Quantitative Analysis"):
        words, matrix, freq = process_kh_analysis(df, col)
        
        t1, t2 = st.tabs(["Word Cloud", "Co-occurrence Matrix"])
        with t1:
            st.image(generate_wordcloud_obj(freq).to_array())
        with t2:
            st.write("Correlation of top words")
            corr_df = pd.DataFrame(matrix[:15, :15], index=words[:15], columns=words[:15])
            st.dataframe(corr_df.style.background_gradient(cmap='Blues'))