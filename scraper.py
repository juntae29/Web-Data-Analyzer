import arxiv
import pandas as pd
import os
import time

def run_web_scraper(search_query, num_papers):
    # 기존 데이터 삭제
    if os.path.exists("scraped_data.csv"): 
        os.remove("scraped_data.csv")
    
    try:
        # 공식 Client 설정: 요청 간 3초 지연으로 가이드라인 준수
        client = arxiv.Client(
            page_size=100, 
            delay_seconds=3.0, 
            num_retries=3
        )
        
        search = arxiv.Search(
            query=search_query,
            max_results=num_papers,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        extracted = []
        # 공식 API 결과 순회
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
        print(f"API Access Error: {e}")
        return False