# 기존 t1, t2, t3 = st.tabs(...) 부분을 아래로 대체
# HTML 스타일을 입혀 글자 크기를 키운 탭 구성
tab1_title = '<span style="font-size: 20px; font-weight: bold;">Dashboard (WordCloud)</span>'
tab2_title = '<span style="font-size: 20px; font-weight: bold;">Keyword List</span>'
tab3_title = '<span style="font-size: 20px; font-weight: bold;">Co-occurrence Network</span>'

t1, t2, t3 = st.tabs([tab1_title, tab2_title, tab3_title])

with t1:
    st.image(generate_wordcloud(freq).to_array())

with t2:
    # 데이터프레임 헤더나 텍스트도 크게 표시 가능
    st.markdown("### <span style='font-size: 24px;'>Top 20 Keywords</span>", unsafe_allow_html=True)
    st.table(word_df.sort_values('Score', ascending=False).head(20))

with t3:
    st.markdown("### <span style='font-size: 24px;'>Word Co-occurrence Correlation Matrix</span>", unsafe_allow_html=True)
    st.dataframe(corr_df.style.background_gradient(cmap='Blues'))