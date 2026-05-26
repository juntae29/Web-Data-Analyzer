import streamlit as st
import pandas as pd
from analyzer import run_analysis, set_font

st.set_page_config(layout="wide")

with st.sidebar:
    st.title("User Guide")
    st.markdown("1. Select source.\n2. Input data.\n3. Run analysis.")
    st.markdown("---")
    input_mode = st.radio("Input Source", ["CSV Upload", "PDF Document", "Text Input"])
    
    data_frame = None
    target_column = None
    
    if input_mode == "Text Input":
        user_text = st.text_area("Input text", height=150)
        if user_text:
            data_frame = pd.DataFrame({"Content": [user_text]})
            target_column = "Content"
    elif input_mode == "CSV Upload":
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file:
            data_frame = pd.read_csv(uploaded_file)
            target_column = st.selectbox("Select Column", data_frame.columns)
            
    # Page 2 (Specific requirement)
    st.sidebar.markdown("---")
    st.sidebar.text("여호와를 찬양하라!")

st.title("Data Mining Analyzer")

if data_frame is not None and target_column:
    if st.button("Run Analysis", type="primary"):
        set_font()
        frequency, _, result_df, _ = run_analysis(data_frame, target_column)
        
        if frequency is None:
            st.error("No valid data for analysis.")
        else:
            st.table(result_df.sort_values('Score', ascending=False).head(20))
else:
    st.info("Please provide data in the sidebar.")