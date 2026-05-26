import requests
import feedparser
import pandas as pd
import os

def run_web_scraper(search_query, num_papers):
    if os.path.exists("scraped_data.csv"): 
        os.remove("scraped_data.csv")
    
    # arXiv RSS 피드 URL
    query = search_query.replace(' ', '+')
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={num_papers}&sortBy=submittedDate&sortOrder=descending"
    
    try:
        response = requests.get(url, timeout=15)
        feed = feedparser.parse(response.content)
        
        extracted = []
        for entry in feed.entries:
            extracted.append({
                "title": entry.title,
                "Abstract": entry.summary
            })
            
        if not extracted: 
            return False
            
        pd.DataFrame(extracted).to_csv("scraped_data.csv", index=False, encoding="utf-8-sig")
        return True
    except Exception as e:
        print(f"RSS Parsing Error: {e}")
        return False