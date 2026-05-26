import streamlit as st
import pandas as pd
from scraper import run_web_scraper
from analyzer import process_dataframe_mining, generate_wordcloud_obj
import os

# 1. Page Configuration (Must be at the top)
st.set_page_config(
    page_title="Multi-Source Text Data Mining Analyzer",
    page_icon="🌐",
    layout="wide"
)

# 2. Session State Management
if "interacted" not in st.session_state:
    st.session_state["interacted"] = False

# 3. Global Title & Description
st.title("🌐 Multi-Source Text Data Mining Analyzer")
st.caption("This system executes advanced text mining analytics from academic web sources, PDF documents, and custom inputs.")
st.markdown("---")

# 4. Sidebar Control Panel
with st.sidebar:
    st.header("⚙️ Global Control Panel")
    analysis_mode = st.selectbox("Select Analysis Mode", ["arXiv Web Scraping", "PDF Document Analysis", "Custom Text Input"])
    st.subheader("Scraping Parameters")
    keyword = st.text_input("Enter Research Keyword", value="Artificial Intelligence")
    num_papers = st.slider("Number of Papers to Fetch", 10, 100, 30)
    launch_btn = st.button("Launch Real-time Scraping & Analytics")

# 5. Main Dashboard Logic
if launch_btn:
    st.session_state["interacted"] = True
    st.subheader(f"📊 Dataset Overview (Total Records: {num_papers})")
    
    with st.spinner("Executing Text Mining & Keyword Extraction..."):
        # Scrape and Process
        if run_web_scraper(keyword, num_papers):
            df = pd.read_csv("scraped_data.csv")
            word_df, words = process_dataframe_mining(df)
            wc = generate_wordcloud_obj(words)
            
            # Display Results
            col1, col2 = st.columns(2)
            with col1:
                st.write("### 📊 Word Cloud Visualization")
                st.image(wc.to_array(), use_container_width=True)
            with col2:
                st.write("### 📝 Top 10 Keywords")
                st.dataframe(word_df, use_container_width=True)
            
            st.subheader("Raw Data Preview")
            st.dataframe(df, use_container_width=True)
            st.success(f"Analysis successfully completed for keyword: **{keyword}**.")
        else:
            st.error("Failed to retrieve data. Please check your connection or try another keyword.")
else:
    if not st.session_state["interacted"]:
        st.info("👈 Use the sidebar control panel to enter a keyword and click 'Launch Real-time Scraping & Analytics' to start the dashboard analysis.")