import arxiv
import pandas as pd
import os

def run_web_scraper(search_query, num_papers):
    if os.path.exists("scraped_data.csv"): os.remove("scraped_data.csv")
    try:
        client = arxiv.Client(delay_seconds=3.0, num_retries=3)
        # 1차 시도: 사용자의 검색어
        search = arxiv.Search(query=search_query, max_results=num_papers, sort_by=arxiv.SortCriterion.SubmittedDate)
        results = list(client.results(search))
        
        # 결과가 없으면 2차 시도: 최근 논문 전체 검색 (폴백)
        if not results:
            fallback_search = arxiv.Search(query="* ", max_results=10, sort_by=arxiv.SortCriterion.SubmittedDate)
            results = list(client.results(fallback_search))
            
        extracted = [{"title": r.title, "Abstract": r.summary} for r in results]
        if not extracted: return False
        
        pd.DataFrame(extracted).to_csv("scraped_data.csv", index=False, encoding="utf-8-sig")
        return True
    except: return False

def scrape_text_from_url(url):
    import requests
    from bs4 import BeautifulSoup
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ').strip()
    except: return None