import streamlit as st
import pandas as pd
import os
from scraper import run_web_scraper, scrape_text_from_url
from analyzer import process_dataframe_mining, generate_wordcloud_obj

st.set_page_config(layout="wide")
st.title("🌐 Text Data Mining Analyzer")

with st.sidebar:
    mode = st.selectbox("Mode", ["arXiv Web Scraping", "Text Input"])
    keyword = st.text_input("Keyword", "Artificial Intelligence")
    num = st.slider("Papers", 10, 50, 20)

if st.button("Launch"):
    if mode == "arXiv Web Scraping":
        if run_web_scraper(keyword, num):
            df = pd.read_csv("scraped_data.csv")
            st.success(f"Successfully loaded {len(df)} papers.")
            word_df, words = process_dataframe_mining(df)
            st.image(generate_wordcloud_obj(words).to_array())
            st.dataframe(df)
        else:
            st.error("Scraping failed. arXiv may be blocking this server's IP.")
    else:
        st.info("Please use Text Input mode for testing.")