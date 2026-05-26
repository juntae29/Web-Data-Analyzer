import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def run_web_scraper(search_query, num_papers):
    extracted_records = []
    start_index = 0
    headers = {"User-Agent": "Mozilla/5.0"}
    while len(extracted_records) < num_papers:
        url = f"https://arxiv.org/search/?query={search_query.replace(' ', '+')}&size=50&start={start_index}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("li", class_="arxiv-result")
            if not articles: break
            for article in articles:
                if len(extracted_records) >= num_papers: break
                title = article.find("p", class_="title").text.strip()
                summary = article.find("p", class_="abstract").text.replace("Abstract:", "").strip()
                extracted_records.append({"title": title, "Abstract": summary})
            start_index += 50
            time.sleep(0.5)
        except: break
    pd.DataFrame(extracted_records).to_csv("scraped_data.csv", index=False, encoding="utf-8-sig")
    return True

def scrape_text_from_url(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for e in soup(["script", "style", "nav", "footer", "header"]): e.extract()
        return re.sub(r'\s+', ' ', soup.get_text(separator=' ')).strip()
    except: return None