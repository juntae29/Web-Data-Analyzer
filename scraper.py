import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from urllib.parse import quote

def run_web_scraper(search_query, num_papers):
    extracted_records = []
    start_index = 0
    # 파일 잔류 문제 방지
    if os.path.exists("scraped_data.csv"): 
        os.remove("scraped_data.csv")
    
    # 브라우저 위장 헤더
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    encoded_query = quote(search_query)
    
    while len(extracted_records) < num_papers:
        url = f"https://arxiv.org/search/?query={encoded_query}&size=50&start={start_index}"
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("li", class_="arxiv-result")
            if not articles: 
                break
                
            for article in articles:
                if len(extracted_records) >= num_papers: 
                    break
                title_el = article.find("p", class_="title")
                summary_el = article.find("p", class_="abstract")
                
                if title_el and summary_el:
                    title = title_el.text.strip()
                    summary = summary_el.text.replace("Abstract:", "").strip()
                    extracted_records.append({"title": title, "Abstract": summary})
            
            start_index += 50
            time.sleep(3.0) # 서버 부하 방지를 위해 지연 시간 추가
        except: 
            break
    
    if not extracted_records: 
        return False
        
    pd.DataFrame(extracted_records).to_csv("scraped_data.csv", index=False, encoding="utf-8-sig")
    return True

def scrape_text_from_url(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if response.status_code != 200: 
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        for e in soup(["script", "style", "nav", "footer", "header"]): 
            e.extract()
        text = soup.get_text(separator=' ').strip()
        return text if len(text) > 50 else None
    except: 
        return None