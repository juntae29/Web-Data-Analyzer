import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pypdf import PdfReader
from analyzer import run_quantitative_analysis, generate_wordcloud, set_matplotlib_font

st.set_page_config(layout="wide")

# 1. 사이드바: 가이드와 입력 위젯을 모두 배치 (레이아웃 간섭 원천 차단)
with st.sidebar:
    st.title("💡 User Guide")
    st.markdown("1. Select Input Source.\n2. Upload/Input Data.\n3. Press Run Analysis.")
    st.markdown("---")
    
    input_mode = st.radio("Input Source", ["CSV Upload", "PDF Document", "Text Input"])
    st.markdown("---")
    
    # 입력 위젯을 사이드바에 배치하여 메인 화면 제목을 침범하지 않게 함
    data_frame = None
    target_column = None
    
    if input_mode == "Text Input":
        user_text = st.text_area("Paste text here", height=150)
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

# 2. 메인 화면: 오직 분석 결과만 표시
st.title("Data Mining Analyzer")

if data_frame is not None:
    if st.button("Run Analysis", type="primary"):
        set_matplotlib_font()
        frequency, correlation_df, word_score_df, graph = run_quantitative_analysis(data_frame, target_column)
        
        tab1, tab2, tab3 = st.tabs(["Dashboard", "Keyword List", "Network"])
        with tab1:
            if frequency: st.image(generate_wordcloud(frequency).to_array())
        with tab2:
            st.table(word_score_df.sort_values('Score', ascending=False).head(20))
        with tab3:
            if graph and len(graph.nodes) > 0:
                fig, ax = plt.subplots(figsize=(8, 6))
                pos = nx.spring_layout(graph, k=0.5)
                nx.draw(graph, pos, with_labels=True, node_color='skyblue', ax=ax, font_family='NanumGothic')
                st.pyplot(fig)
            else: st.warning("Insufficient data.")
else:
    st.info("Please select an input source and provide data in the sidebar to start.")