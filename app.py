import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pypdf import PdfReader
from analyzer import run_quantitative_analysis, generate_wordcloud, set_matplotlib_font

st.set_page_config(layout="wide")

# 1. 안내 문구는 사이드바로 완전히 이동하여 레이아웃 간섭 제거
with st.sidebar:
    st.title("💡 User Guide")
    st.markdown("""
    1. Select input method.
    2. Input/Upload data in the main section.
    3. Click 'Run Analysis' to see results.
    """)
    st.markdown("---")
    input_mode = st.radio("Input Source", ["CSV Upload", "PDF Document", "Text Input"])

# 2. 메인 화면을 상단(제목)과 하단(분석 영역)으로 분리 (Colums 사용)
st.title("Data Mining Analyzer")
st.markdown("---")

# 3. 분석을 위한 메인 컨테이너 고정
main_container = st.container()

with main_container:
    data_frame = None
    target_column = None

    # 입력 위젯 배치
    if input_mode == "Text Input":
        user_text = st.text_area("Input text for analysis", placeholder="Paste your text here.", height=150)
        if user_text: 
            data_frame = pd.DataFrame({"Content": [user_text]})
            target_column = "Content"
    elif input_mode == "CSV Upload":
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file: 
            data_frame = pd.read_csv(uploaded_file)
            target_column = st.selectbox("Select Column", data_frame.columns)
    elif input_mode == "PDF Document":
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded_file:
            reader = PdfReader(uploaded_file)
            text_content = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            data_frame = pd.DataFrame({"Content": [text_content]})
            target_column = "Content"

    # 4. 분석 실행 및 결과 섹션 분리
    st.markdown("---")
    set_matplotlib_font()
    if data_frame is not None:
        if input_mode != "CSV Upload":
            st.write(f"**Target Column:** '{target_column}'")
        
        if st.button("Run Analysis", type="primary"):
            frequency, correlation_df, word_score_df, graph = run_quantitative_analysis(data_frame, target_column)
            
            # 결과 섹션: Tab을 사용하여 시각적 분리
            tabs = st.tabs(["Dashboard (WordCloud)", "Keyword List", "Co-occurrence Network"])
            
            with tabs[0]:
                if frequency: st.image(generate_wordcloud(frequency).to_array())
            with tabs[1]:
                st.table(word_score_df.sort_values('Score', ascending=False).head(20))
            with tabs[2]:
                if graph and len(graph.nodes) > 0:
                    fig, ax = plt.subplots(figsize=(10, 8))
                    pos = nx.spring_layout(graph, k=0.5)
                    nx.draw(graph, pos, with_labels=True, node_color='skyblue', font_size=12, ax=ax, font_family='NanumGothic')
                    st.pyplot(fig)
                else: st.warning("Insufficient data.")