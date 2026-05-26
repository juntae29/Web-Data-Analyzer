import streamlit as st
import pandas as pd
from pypdf import PdfReader
from analyzer import run_quantitative_analysis, generate_wordcloud
# scraper 모듈이 있다면 여기서 import, 없으면 기본 기능 유지

st.set_page_config(layout="wide")
st.title("Data Mining Analyzer (KH Coder Integrated)")

mode = st.sidebar.radio("Input Source", ["CSV Upload", "PDF Document", "Text Input"])
df = None

if mode == "CSV Upload":
    f = st.file_uploader("Upload CSV", type=["csv"])
    if f: df = pd.read_csv(f)
elif mode == "PDF Document":
    f = st.file_uploader("Upload PDF", type=["pdf"])
    if f:
        reader = PdfReader(f)
        text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
        df = pd.DataFrame({"Content": [text]})
elif mode == "Text Input":
    t = st.text_area("Paste Text")
    if t: df = pd.DataFrame({"Content": [t]})

if df is not None:
    col = st.selectbox("Select Column", df.columns)
    if st.button("Run Analysis"):
        freq, corr_df, word_df = run_quantitative_analysis(df, col)
        t1, t2, t3 = st.tabs(["WordCloud", "Keyword List", "Co-occurrence Network"])
        with t1: st.image(generate_wordcloud(freq).to_array())
        with t2: st.table(word_df.sort_values('Score', ascending=False).head(20))
        with t3: st.dataframe(corr_df.style.background_gradient(cmap='Blues'))