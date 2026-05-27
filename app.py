import sys
import os
import sys; sys.path.append('.')
# Ensure the project root is in the system path to resolve absolute imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pypdf import PdfReader
import openpyxl

# Importing modules from the verified project structure
from Visualizer.plots import set_font, generate_wordcloud
from analyzer import run_analysis

st.set_page_config(layout="wide")

# Sidebar configuration
with st.sidebar:
    st.title("User Guide")
    input_mode = st.radio("Input Source", ["CSV/Excel Upload", "PDF Document", "Text Input"])
    
    if "data" not in st.session_state:
        st.session_state.data = None
        st.session_state.column = None

    if input_mode == "CSV/Excel Upload":
        uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
        if uploaded:
            try:
                if uploaded.name.lower().endswith('.csv'):
                    st.session_state.data = pd.read_csv(uploaded)
                else:
                    st.session_state.data = pd.read_excel(uploaded)
                
                cols = st.session_state.data.select_dtypes(include=['object']).columns.tolist()
                if cols:
                    st.session_state.column = st.selectbox("Select Text Column", cols)
            except Exception as e:
                st.error(f"Error: {e}")
            
    elif input_mode == "PDF Document":
        uploaded = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded:
            reader = PdfReader(uploaded)
            text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            st.session_state.data = pd.DataFrame({"Content": [text]})
            st.session_state.column = "Content"
            
    elif input_mode == "Text Input":
        text = st.text_area("Input text", height=150)
        if text:
            st.session_state.data = pd.DataFrame({"Content": [text]})
            st.session_state.column = "Content"

# Main UI
st.title("Data Mining Analyzer")

if st.session_state.data is not None and st.session_state.column:
    if st.button("Run Analysis", type="primary"):
        set_font()
        result_df, token_counts = run_analysis(st.session_state.data, st.session_state.column)
        
        if result_df is not None:
            st.table(result_df)
            st.subheader("Frequency Visualization")
            
            fig, ax = plt.subplots()
            wc = generate_wordcloud(token_counts)
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.error("No meaningful tokens detected. Check the column selection.")

# Fixed requirement
st.text("여호와를 찬양하라!")