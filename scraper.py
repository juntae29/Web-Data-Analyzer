import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

def run_web_scraper(search_query, num_papers):
    if os.path.exists("scraped_data.csv"): os.remove("scraped_data.csv")
    
    # 봇으로 간주되지 않도록 상세한 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://arxiv.org/"
    }
    
    query = search_query.replace(' ', '+')
    # RSS 대신 검색 결과 페이지를 직접 파싱
    url = f"https://arxiv.org/search/?query={query}&searchtype=all&source=header&size={num_papers}&order=-announced_date_first"
    
    try:
        time.sleep(2)  # 요청 간격 두기
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("li", class_="arxiv-result")
        
        extracted = []
        for article in articles:
            title = article.find("p", class_="title").text.strip()
            summary = article.find("p", class_="abstract").text.replace("Abstract:", "").strip()
            extracted.append({"title": title, "Abstract": summary})
            
        if not extracted: return False
        pd.DataFrame(extracted).to_csv("scraped_data.csv", index=False, encoding="utf-8-sig")
        return True
    except Exception as e:
        print(f"Scraping Error: {e}")
        return False