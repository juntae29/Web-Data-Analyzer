import arxiv
import pandas as pd
import os

def run_web_scraper(search_query, num_papers):
    # 기존 파일 삭제
    if os.path.exists("scraped_data.csv"): 
        os.remove("scraped_data.csv")
    
    try:
        # 공식 API를 사용하여 데이터 요청
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
            
        # 결과 저장
        pd.DataFrame(extracted).to_csv("scraped_data.csv", index=False, encoding="utf-8-sig")
        return True
    except Exception as e:
        print(f"API Error: {e}")
        return False

def scrape_text_from_url(url):
    # 이 함수는 필요시 보완
    return None