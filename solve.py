import argparse
import csv
import requests
import re
import logging
import xml.etree.ElementTree as ET
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# PubMed API URLs
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# API Credentials
EMAIL = "edu.vinay123@gmail.com"
API_KEY = "7bf99b523ee7777caf17e249853552d52d08"

def fetch_pubmed_ids(query: str) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10,
        "email": EMAIL,
        "api_key": API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch PubMed IDs: {e}")
        return []

def fetch_paper_details(pubmed_ids: List[str]) -> str:
    if not pubmed_ids:
        return ""
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml",
        "email": EMAIL,
        "api_key": API_KEY
    }
    try:
        response = requests.get(FETCH_URL, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch PubMed details: {e}")
        return ""

def extract_paper_info(xml_data: str) -> List[Dict[str, Any]]:
    if not xml_data:
        return []
    try:
        root = ET.fromstring(xml_data)
        papers = []
        for article in root.findall(".//PubmedArticle"):
            paper_id = article.find(".//PMID").text if article.find(".//PMID") else "N/A"
            title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") else "N/A"
            publication_date = article.find(".//PubDate/Year")
            publication_date = publication_date.text if publication_date else "Unknown"
            papers.append({
                "PubmedID": paper_id,
                "Title": title,
                "Publication Date": publication_date
            })
        return papers
    except ET.ParseError as e:
        logging.error(f"XML parsing error: {e}")
        return []

def save_to_csv(papers: List[Dict[str, Any]], filename: str):
    if not papers:
        return
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["PubmedID", "Title", "Publication Date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(papers)
        logging.info(f"Results saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")

def display_results(papers: List[Dict[str, Any]]):
    if not papers:
        return
    for paper in papers:
        print(f"PubmedID: {paper['PubmedID']}")
        print(f"Title: {paper['Title']}")
        print(f"Publication Date: {paper['Publication Date']}")
        print("-----------------------------")

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers based on a search query.")
    parser.add_argument("query", type=str, help="PubMed search query.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    
    args = parser.parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    pubmed_ids = fetch_pubmed_ids(args.query)
    xml_data = fetch_paper_details(pubmed_ids)
    papers = extract_paper_info(xml_data)
    
    if args.file:
        save_to_csv(papers, args.file)
    else:
        display_results(papers)

if __name__ == "__main__":
    main()