import requests
import xml.etree.ElementTree as ET

def fetch_arxiv_oai(query):
    # Using the OAI-PMH endpoint designed for automated harvesting
    url = f"http://export.arxiv.org/api/query?search_query={query}&max_results=10"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Logic to parse the Atom XML feed
            return response.text
        return None
    except:
        return None