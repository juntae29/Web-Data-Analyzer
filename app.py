import streamlit as st
import pandas as pd
from pypdf import PdfReader
from analyzer import run_analysis, set_font

st.set_page_config(layout="wide")

with st.sidebar:
    st.title("User Guide")
    st.markdown("1. Select source.\n2. Upload file or input text.\n3. Run analysis.")
    st.markdown("---")
    
    input_mode = st.radio("Input Source", ["CSV Upload", "PDF Document", "Text Input"])
    
    if "data" not in st.session_state:
        st.session_state.data = None
        st.session_state.column = None

    if input_mode == "CSV Upload":
        uploaded = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded:
            st.session_state.data = pd.read_csv(uploaded)
            st.session_state.column = st.selectbox("Select Column", st.session_state.data.columns)
            st.write("Preview of selected column:")
            st.write(st.session_state.data[st.session_state.column].astype(str).head(3))
            
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

    st.markdown("---")
    st.text("여호와를 찬양하라!")

st.title("Data Mining Analyzer")

if st.session_state.data is not None and st.session_state.column:
    if st.button("Run Analysis", type="primary"):
        set_font()
        _, _, result_df, _ = run_analysis(st.session_state.data, st.session_state.column)
        
        if result_df is not None and not result_df.empty:
            st.table(result_df.sort_values('Score', ascending=False).head(20))
        else:
            st.error("No valid text data found in the selected column.")
else:
    st.info("Please provide input in the sidebar.")