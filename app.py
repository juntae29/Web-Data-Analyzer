import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pypdf import PdfReader
from analyzer import run_quantitative_analysis, generate_wordcloud, set_matplotlib_font

st.set_page_config(layout="wide")

# 1. Sidebar for Instructions (to prevent layout collision)
with st.sidebar:
    st.title("💡 User Guide")
    st.markdown("""
    1. Select the input method from the radio buttons below.
    2. Input your data or text in the main section.
    3. Click 'Run Analysis' to generate insights.
    """)
    st.markdown("---")
    input_mode = st.radio("Input Source", ["CSV Upload", "PDF Document", "Text Input"])

# 2. Main Title
st.title("Data Mining Analyzer")
st.markdown("---")

# 3. Dynamic Input Area (Always positioned below title)
data_frame = None
target_column = None

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

# 4. Analysis Execution
set_matplotlib_font()
if data_frame is not None:
    if input_mode != "CSV Upload":
        st.write(f"**Target Column:** '{target_column}'")
    
    if st.button("Run Analysis", type="primary"):
        frequency, correlation_df, word_score_df, graph = run_quantitative_analysis(data_frame, target_column)
        
        tab1, tab2, tab3 = st.tabs(["Dashboard (WordCloud)", "Keyword List", "Co-occurrence Network"])
        
        with tab1:
            if frequency: st.image(generate_wordcloud(frequency).to_array())
        with tab2:
            st.table(word_score_df.sort_values('Score', ascending=False).head(20))
        with tab3:
            if graph and len(graph.nodes) > 0:
                figure, axis = plt.subplots(figsize=(10, 8))
                positions = nx.spring_layout(graph, k=0.5)
                nx.draw(graph, positions, with_labels=True, node_color='skyblue', font_size=12, ax=axis, font_family='NanumGothic')
                st.pyplot(figure)
            else: st.warning("Insufficient data for network visualization.")