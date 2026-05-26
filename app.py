import streamlit as st
import pandas as pd
import os
from scraper import run_web_scraper
from analyzer import process_dataframe_mining, generate_wordcloud_obj

st.set_page_config(page_title="arXiv Data Analyzer", layout="wide")
st.title("🌐 arXiv Data Mining Analyzer")

with st.sidebar:
    st.header("Configuration")
    keyword = st.text_input("Research Keyword", "Artificial Intelligence")
    num = st.slider("Number of Papers", 10, 50, 20)

if st.button("Launch Analysis"):
    with st.spinner("Fetching data from arXiv API..."):
        if run_web_scraper(keyword, num):
            df = pd.read_csv("scraped_data.csv")
            st.success(f"Successfully loaded {len(df)} papers.")
            
            # 분석 및 시각화
            word_df, words = process_dataframe_mining(df)
            wc = generate_wordcloud_obj(words)
            
            tab1, tab2 = st.tabs(["Visualization", "Raw Data"])
            with tab1:
                st.image(wc.to_array(), use_column_width=True)
                st.bar_chart(word_df.set_index("Word"))
            with tab2:
                st.dataframe(df)
        else:
            st.error("Failed to fetch data from arXiv API. Please try again.")