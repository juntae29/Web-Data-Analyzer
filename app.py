import streamlit as st
import pandas as pd
from scraper import run_web_scraper, scrape_text_from_url
from analyzer import process_dataframe_mining, generate_wordcloud_obj
from pypdf import PdfReader

st.set_page_config(page_title="Multi-Source Text Data Mining Analyzer", layout="wide", page_icon="🌐")

st.title("🌐 Multi-Source Text Data Mining Analyzer")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Global Control Panel")
    analysis_mode = st.selectbox(
        "Select Analysis Mode", 
        ["arXiv Web Scraping", "PDF Document Analysis", "Custom Text Input", "Web URL Analysis"]
    )
    
    if analysis_mode == "arXiv Web Scraping":
        keyword = st.text_input("Enter Research Keyword", value="Artificial Intelligence")
        num_papers = st.slider("Number of Papers to Fetch", 10, 100, 30)
        launch_btn = st.button("Launch Analysis")
        mode_data = {"type": "web", "keyword": keyword, "num": num_papers}
        
    elif analysis_mode == "PDF Document Analysis":
        uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])
        launch_btn = st.button("Analyze PDF")
        mode_data = {"type": "pdf", "file": uploaded_file}
        
    elif analysis_mode == "Web URL Analysis":
        url_input = st.text_input("Enter Website URL")
        keyword_input = st.text_input("Focus Keyword (Optional)")
        launch_btn = st.button("Analyze Website")
        mode_data = {"type": "url", "url": url_input, "keyword": keyword_input}
        
    else: # Custom Text Input
        custom_text = st.text_area("Paste your text here", height=200)
        launch_btn = st.button("Analyze Text")
        mode_data = {"type": "text", "content": custom_text}

if launch_btn:
    df = None
    with st.spinner("Processing..."):
        if mode_data["type"] == "web":
            if run_web_scraper(mode_data["keyword"], mode_data["num"]):
                df = pd.read_csv("scraped_data.csv")
        elif mode_data["type"] == "pdf" and mode_data["file"] is not None:
            reader = PdfReader(mode_data["file"])
            text = "".join([page.extract_text() for page in reader.pages])
            df = pd.DataFrame({"Abstract": [text]})
        elif mode_data["type"] == "url" and mode_data["url"]:
            full_text = scrape_text_from_url(mode_data["url"])
            if full_text:
                text = full_text
                if mode_data["keyword"]:
                    sentences = [s.strip() for s in full_text.split('.') if mode_data["keyword"].lower() in s.lower()]
                    text = " ".join(sentences) if sentences else full_text
                df = pd.DataFrame({"Abstract": [text]})
        elif mode_data["type"] == "text" and mode_data["content"]:
            df = pd.DataFrame({"Abstract": [mode_data["content"]]})
            
    if df is not None and not df.empty:
        word_df, words = process_dataframe_mining(df)
        wc = generate_wordcloud_obj(words)
        col1, col2 = st.columns(2)
        with col1:
            st.image(wc.to_array(), use_column_width=True)
        with col2:
            st.bar_chart(word_df.set_index("Word"))
        st.dataframe(df.head(10))
    else:
        st.error("분석 데이터를 생성할 수 없다. 입력값을 확인하라.")