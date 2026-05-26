import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

def run_web_scraper(search_query, num_papers):
    if os.path.exists("scraped_data.csv"): os.remove("scraped_data.csv")
    
    # 더 단순한 헤더 사용
    headers = {"User-Agent": "Mozilla/5.0"}
    query = search_query.replace(' ', '+')
    extracted = []
    
    # 50개 단위로 가져오는 대신 한 페이지만 빠르게 처리
    url = f"https://arxiv.org/search/?query={query}&size={num_papers}&order=-announced_date_first"
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("li", class_="arxiv-result")
        
        for article in articles:
            title = article.find("p", class_="title").text.strip()
            summary = article.find("p", class_="abstract").text.replace("Abstract:", "").strip()
            extracted.append({"title": title, "Abstract": summary})
            
        if not extracted: return False
        pd.DataFrame(extracted).to_csv("scraped_data.csv", index=False, encoding="utf-8-sig")
        return True
    except:
        return False

def scrape_text_from_url(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ').strip()
    except: return None