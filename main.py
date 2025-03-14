import argparse
import csv
import requests
import re
from typing import List, Dict, Any

# Corrected URLs
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
EMAIL = "edu.vinay123@gmail.com"
API_KEY = "7bf99b523ee7777caf17e249853552d52d08"  # Replace with your actual API key

def fetch_pubmed_ids(query: str) -> List[str]:
    """
    Fetch PubMed IDs for the given query.
    """
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10,
        "email": EMAIL,
        "api_key": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch details for a list of PubMed IDs.
    """
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml",
        "email": EMAIL,
        "api_key": API_KEY
    }
    response = requests.get(FETCH_URL, params=params)
    response.raise_for_status()
    return response.text  # Returning raw XML response for parsing

def is_non_academic(affiliation: str) -> bool:
    """
    Determine if an author is affiliated with a pharmaceutical/biotech company.
    """
    academic_keywords = ["university", "college", "institute", "school", "lab", "hospital"]
    return not any(word in affiliation.lower() for word in academic_keywords)

def extract_paper_info(xml_data: str) -> List[Dict[str, Any]]:
    """
    Extract relevant information from PubMed XML response.
    """
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_data)

    papers = []
    for article in root.findall(".//PubmedArticle"):
        paper_id = article.find(".//PMID").text if article.find(".//PMID") is not None else ""
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else ""
        publication_date = article.find(".//PubDate/Year")
        publication_date = publication_date.text if publication_date is not None else "Unknown"
        
        non_academic_authors = []
        company_affiliations = []
        corresponding_email = ""

        for author in article.findall(".//Author"):
            name = author.find("LastName").text if author.find("LastName") is not None else "Unknown"
            affiliation = author.find("AffiliationInfo/Affiliation")
            affiliation_text = affiliation.text if affiliation is not None else ""

            if is_non_academic(affiliation_text):
                non_academic_authors.append(name)
                company_affiliations.append(affiliation_text)

            email_match = re.search(r"[\w\.-]+@[\w\.-]+", affiliation_text)
            if email_match:
                corresponding_email = email_match.group(0)

        papers.append({
            "PubmedID": paper_id,
            "Title": title,
            "Publication Date": publication_date,
            "Non-academic Author(s)": "; ".join(non_academic_authors),
            "Company Affiliation(s)": "; ".join(company_affiliations),
            "Corresponding Author Email": corresponding_email,
        })

    return papers

def save_to_csv(papers: List[Dict[str, Any]], filename: str):
    """
    Save results to a CSV file.
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", type=str, help="PubMed search query.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()

    try:
        pubmed_ids = fetch_pubmed_ids(args.query)
        if args.debug:
            print(f"Fetched PubMed IDs: {pubmed_ids}")
        
        xml_data = fetch_paper_details(pubmed_ids)
        papers = extract_paper_info(xml_data)
        
        if args.file:
            save_to_csv(papers, args.file)
            print(f"Results saved to {args.file}")
        else:
            for paper in papers:
                print(paper)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
