import streamlit as st
import pandas as pd
from scraper import scrape_text_from_url
from analyzer import process_advanced_mining, generate_wordcloud_obj, map_taxonomy
from pypdf import PdfReader

st.set_page_config(layout="wide")
st.title("Advanced Data Mining Analyzer")

# 1. Sidebar Configuration
with st.sidebar:
    st.header("Mode Selection")
    mode = st.radio("Choose Input Method", ["CSV Upload", "PDF Document", "Custom Text Input", "Web URL"])
    st.divider()
    st.header("Taxonomy Settings")
    cat_name = st.text_input("Category Name", "Methodology")
    cat_words = st.text_input("Keywords", "regression, analysis, model")

# 2. Data Loading Logic
df = None

if mode == "CSV Upload":
    f = st.file_uploader("Upload CSV file", type=["csv"])
    if f: df = pd.read_csv(f)

elif mode == "PDF Document":
    f = st.file_uploader("Upload PDF file", type=["pdf"])
    if f:
        reader = PdfReader(f)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        df = pd.DataFrame({"Content": [text]})

elif mode == "Custom Text Input":
    t = st.text_area("Enter text to analyze", height=200)
    if st.button("Submit Text"):
        if t: df = pd.DataFrame({"Content": [t]})

elif mode == "Web URL":
    u = st.text_input("Enter URL")
    q = st.text_input("Enter Search Query")
    if st.button("Fetch URL Content"):
        text = scrape_text_from_url(u, q)
        if text: df = pd.DataFrame({"Content": [text]})
        else: st.error("Failed to fetch URL.")

# 3. Analysis Execution
if df is not None and not df.empty:
    st.success("Data Loaded Successfully")
    selected_col = st.selectbox("Select column to analyze:", df.columns)
    
    if st.button("Start Advanced Analysis"):
        word_df, word_dict = process_advanced_mining(df, selected_col)
        
        if not word_df.empty:
            col1, col2 = st.columns(2)
            with col1: st.image(generate_wordcloud_obj(word_dict).to_array())
            with col2: st.bar_chart(word_df.set_index("Word"))
            
            tax_dict = {cat_name: [w.strip().lower() for w in cat_words.split(",")]}
            mapping = map_taxonomy(word_dict.keys(), tax_dict)
            st.write(f"**{cat_name}** Mapping Result:", mapping[cat_name])
        else:
            st.error("Analysis failed. Please check the data.")