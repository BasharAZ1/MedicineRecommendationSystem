import requests
from bs4 import BeautifulSoup

def extract_titles_and_hrefs_from_page(url):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    titles_and_hrefs = []
    for span in soup.find_all('span', class_='title'):
        title = span.text
        href = span.find_parent('a')['href']
        titles_and_hrefs.append((title, href))
    
    return titles_and_hrefs

def extract_all_titles_and_hrefs(base_url):
    all_titles_and_hrefs = []
    current_page = 1
    while True:
        url = f"{base_url}?page={current_page}"
        titles_and_hrefs = extract_titles_and_hrefs_from_page(url)
        if not titles_and_hrefs:
            break
        all_titles_and_hrefs.extend(titles_and_hrefs)
        current_page += 1
    return all_titles_and_hrefs

base_url = "https://www.infomed.co.il/diseases/"
try:
    titles_and_hrefs = extract_all_titles_and_hrefs(base_url)
    for title, href in titles_and_hrefs:
        print(f"Title: {title}, Href: {'https://www.infomed.co.il/'+href}")
except requests.exceptions.RequestException as e:
    print(f"Failed to retrieve the webpage. Error: {e}")
