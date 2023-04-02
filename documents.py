import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.fia.com'
DOC_LOCATION = '/documents/list/season/season-2023-2042/championships/fia-formula-one-world-championship-14'

def check_for_last_document():
    page = requests.get(BASE_URL+DOC_LOCATION)
    soup = BeautifulSoup(page.content, "html.parser")
    li = soup.find_all("li", {'class': 'document-row'})
    final_set = []
    for x in li:
        final_set.append({'link':x.find("a", href=True)['href'], 'name':x.find("div", {'class':'title'}).get_text()})
    try:
        return final_set[0]
    except IndexError:
        return None

def construct_full_link(doc_link):
    return BASE_URL + doc_link.replace(' ', '%20')
