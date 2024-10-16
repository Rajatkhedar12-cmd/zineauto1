import requests
from bs4 import BeautifulSoup
import csv
import json

# Function to crawl arXiv for recent papers
def crawl_arxiv():
    url = 'https://arxiv.org/list/cs/recent'  # 'cs' for all computer science papers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        papers = []
        for item in soup.find_all('div', class_='meta'):
            title = item.find('div', class_='list-title').text.strip().replace('Title:', '').strip()
            authors = item.find('div', class_='list-authors').text.strip().replace('Authors:', '').strip()
            abstract_url = 'https://arxiv.org' + item.find('a')['href']
            papers.append({
                'title': title,
                'authors': authors,
                'abstract_url': abstract_url,
                'source': 'arXiv'
            })
        return papers
    else:
        print(f"Failed to retrieve content from arXiv (status code: {response.status_code})")
        return []

# Function to crawl bioRxiv for recent papers
def crawl_biorxiv():
    url = 'https://www.biorxiv.org/content/early/recent'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        papers = []
        for item in soup.find_all('div', class_='highwire-cite'):
            title = item.find('span', class_='highwire-cite-title').text.strip()
            authors = item.find('span', class_='highwire-citation-authors').text.strip()
            abstract_url = 'https://www.biorxiv.org' + item.find('a')['href']
            papers.append({
                'title': title,
                'authors': authors,
                'abstract_url': abstract_url,
                'source': 'bioRxiv'
            })
        return papers
    else:
        print(f"Failed to retrieve content from bioRxiv")
        return []

# Function to crawl PubMed for recent papers
def crawl_pubmed():
    url = 'https://pubmed.ncbi.nlm.nih.gov/?term=recent'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        papers = []
        for item in soup.find_all('article', class_='full-docsum'):
            title = item.find('a', class_='docsum-title').text.strip()
            authors = item.find('span', class_='docsum-authors').text.strip()
            abstract_url = 'https://pubmed.ncbi.nlm.nih.gov' + item.find('a')['href']
        
            papers.append({
                'title': title,
                'authors': authors,
                'abstract_url': abstract_url,
                'source': 'PubMed'
            })
        return papers
    else:
        print(f"Failed to retrieve content from PubMed")
        return []

# Function to crawl SSRN for recent papers (not fully defined in your previous code, so I am excluding it for now)
# def crawl_ssrn():
#     ...

# Function to crawl IEEE for recent papers
def crawl_ieee():
    url = 'https://ieeexplore.ieee.org/Xplore/home.jsp'
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve content from IEEE Xplore: {e}")
        return []  # Return an empty list on failure

    soup = BeautifulSoup(response.content, 'html.parser')
    papers = []
    for item in soup.find_all('div', class_='List-results-items'):
        title_element = item.find('a', class_='document-title')
        author_element = item.find('div', class_='author')

        # Ensure elements exist before accessing them
        if title_element and author_element:
            title = title_element.text.strip()
            authors = author_element.text.strip()
            abstract_url = 'https://ieeexplore.ieee.org' + title_element['href']
            papers.append({
                'title': title,
                'authors': authors,
                'abstract_url': abstract_url,
                'source': 'IEEE'
            })
    return papers

# Clean and process the papers
def clean_paper_data(papers):
    clean_data = []
    for paper in papers:
        clean_data.append({
            'title': paper['title'],
            'authors': paper['authors'],
            'abstract_url': paper['abstract_url'],
            'source': paper['source']
        })
    return clean_data

# Function to save the paper data to a CSV file
def save_to_csv(papers, filename):
    keys = papers[0].keys() if papers else []
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(papers)

# Function to save the paper data to a JSON file
def save_to_json(papers, filename):
    with open(filename, 'w') as json_file:
        json.dump(papers, json_file, indent=4)

# Crawl data from various sources and store them
def main():
    arxiv_papers = clean_paper_data(crawl_arxiv())
    biorxiv_papers = clean_paper_data(crawl_biorxiv())
    pubmed_papers = clean_paper_data(crawl_pubmed())
    ieee_papers = clean_paper_data(crawl_ieee())

    all_papers = arxiv_papers + biorxiv_papers + pubmed_papers + ieee_papers

    # Save the collected data
    save_to_csv(all_papers, 'papers.csv')
    save_to_json(all_papers, 'papers.json')

if __name__ == '__main__':
    main()

