def generate_wordcloud_obj(text_list, font_path=None):
    """
    Generates WordCloud object with robust font mapping for Linux (Streamlit Cloud).
    """
    if not font_path:
        # Search for Nanum fonts in standard Linux directories
        linux_fonts = [
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
            "/usr/share/fonts/fonts-nanum/NanumGothic.ttf",
            "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf"
        ]
        for path in linux_fonts:
            if os.path.exists(path):
                font_path = path
                break
    
    text_content = " ".join(text_list)
    
    # Generate WordCloud
    wc = WordCloud(
        font_path=font_path,
        width=800,
        height=500,
        background_color="white",
        colormap="plasma",
        prefer_horizontal=0.9
    )
    
    return wc.generate(text_content)