import requests
from bs4 import BeautifulSoup

def get_link_from_pwc(link):
    links_git = []
    page = requests.get(link)
    print('join')
    soup = BeautifulSoup(page.content, "html5lib")
    try:
        links = soup.find(class_="paper-implementations code-table")
        links = links.find(id='implementations-full-list')
        list_link = links.find_all('a')
    except IndexError:
        return links_git 
    
    for link in list_link:
        link_href = link.get('href')
        if 'https://github.com' in link_href:
            links_git.append(link_href)

    return links_git

