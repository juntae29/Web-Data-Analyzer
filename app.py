import streamlit as st
import pandas as pd
from analyzer import process_advanced_mining, generate_wordcloud_obj, map_taxonomy

st.set_page_config(layout="wide")
st.title("Data Mining Analyzer (Full Feature Restored)")

# 입력 모드
mode = st.sidebar.radio("Input Source", ["CSV Upload", "Text Input"])
df = None
if mode == "CSV Upload":
    f = st.file_uploader("Upload", type=["csv"])
    if f: df = pd.read_csv(f)
else:
    t = st.text_area("Paste Text")
    if t: df = pd.DataFrame({"Content": [t]})

if df is not None:
    col = st.selectbox("Select Column", df.columns)
    cat_name = st.text_input("Category Label", "Target")
    cat_words = st.text_input("Keywords", "분석, 데이터")
    
    if st.button("Analyze"):
        word_df, word_dict = process_advanced_mining(df, col)
        t1, t2 = st.tabs(["Dashboard", "Taxonomy Mapping"])
        with t1:
            st.image(generate_wordcloud_obj(word_dict).to_array())
        with t2:
            st.table(map_taxonomy(word_df, {cat_name: cat_words})[cat_name])