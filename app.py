import streamlit as st
import pandas as pd
from scraper import run_web_scraper

st.title("🌐 Data Mining Analyzer")

if st.button("Launch Analysis"):
    st.write("Running...")
    if run_web_scraper("Artificial Intelligence", 10):
        df = pd.read_csv("scraped_data.csv")
        st.dataframe(df)
    else:
        st.error("Failed to fetch data.")