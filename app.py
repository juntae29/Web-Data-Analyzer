import streamlit as st
import pandas as pd
from pypdf import PdfReader
from analyzer import run_quantitative_analysis, generate_wordcloud

st.set_page_config(layout="wide")

# CSS: Added rule to hide the 'Press Ctrl+Enter' hint
st.markdown("""
    <style>
    button[data-baseweb="tab"] {
        font-size: 20px !important;
        font-weight: bold !important;
    }
    div[data-testid="stTextArea"] label {
        display: none;
    }
    /* Hide the 'Press Ctrl+Enter' hint */
    .st-emotion-cache-1jm61g7 {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Data Mining Analyzer")

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
    t = st.text_area("Paste Text", label_visibility="collapsed")
    if t: df = pd.DataFrame({"Content": [t]})

if df is not None:
    if mode == "CSV Upload":
        col = st.selectbox("Select Column", df.columns)
    else:
        col = "Content"
        st.info(f"Analysis will be performed on the '{col}' column.")

    if st.button("Run Analysis"):
        freq, corr_df, word_df = run_quantitative_analysis(df, col)
        
        t1, t2, t3 = st.tabs(["Dashboard (WordCloud)", "Keyword List", "Co-occurrence Network"])
        
        with t1:
            st.markdown("### Dashboard (WordCloud)")
            if freq: st.image(generate_wordcloud(freq).to_array())
            else: st.warning("No data found.")
        with t2:
            st.markdown("### Keyword List")
            if not word_df.empty: st.table(word_df.sort_values('Score', ascending=False).head(20))
            else: st.warning("No keywords found.")
        with t3:
            st.markdown("### Co-occurrence Network")
            if not corr_df.empty: st.dataframe(corr_df.style.background_gradient(cmap='Blues'))
            else: st.warning("No correlation data found.")