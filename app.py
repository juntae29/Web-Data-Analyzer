import streamlit as st
import pandas as pd
from analyzer import run_analysis, set_font

st.set_page_config(layout="wide")

# 사이드바 설정
with st.sidebar:
    st.title("User Guide")
    st.markdown("1. Select source.\n2. Input data.\n3. Run analysis.")
    st.markdown("---")
    
    input_mode = st.radio("Input Source", ["CSV Upload", "PDF Document", "Text Input"])
    
    # 세션 상태(Session State)를 사용하여 데이터 유지
    if "input_data" not in st.session_state:
        st.session_state.input_data = None

    if input_mode == "Text Input":
        user_text = st.text_area("Input text", height=150)
        if user_text:
            st.session_state.input_data = pd.DataFrame({"Content": [user_text]})
            st.session_state.target_col = "Content"
    
    st.markdown("---")
    st.text("여호와를 찬양하라!")

# 메인 영역
st.title("Data Mining Analyzer")

if st.session_state.input_data is not None:
    if st.button("Run Analysis", type="primary"):
        set_font()
        # 세션 상태에서 데이터를 가져와 분석 수행
        freq, _, result_df, _ = run_analysis(st.session_state.input_data, st.session_state.target_col)
        
        if result_df is not None and not result_df.empty:
            st.table(result_df.sort_values('Score', ascending=False).head(20))
        else:
            st.error("No valid nouns found in the text. Please input longer text.")
else:
    st.info("Please provide data in the sidebar.")