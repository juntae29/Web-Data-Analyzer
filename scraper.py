import arxiv
import pandas as pd
import os

def run_web_scraper(search_query, num_papers):
    if os.path.exists("scraped_data.csv"): 
        os.remove("scraped_data.csv")
    
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=search_query,
            max_results=num_papers,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        extracted = []
        for result in client.results(search):
            extracted.append({
                "title": result.title,
                "Abstract": result.summary
            })
            
        if not extracted: 
            return False
            
        pd.DataFrame(extracted).to_csv("scraped_data.csv", index=False, encoding="utf-8-sig")
        return True
    except Exception as e:
        # API 실패 원인 로그 출력 (View logs에서 확인 가능)
        print(f"API Detailed Error: {e}")
        return False

def scrape_text_from_url(url):
    import requests
    from bs4 import BeautifulSoup
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ').strip()
    except:
        return None