import requests
from bs4 import BeautifulSoup
import time
import re
import Get_arxiv
import Get_pwc

# Some parts of HTML don't contain the necessary content
blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
    ]

def Google_find_links(paper_name):
    results = 100

    # Scientific paper can be found in GOOGLE and GOOGLE SCHOLAR
    page_google = requests.get(f"https://www.google.com/search?q={paper_name}&num={results}")
    soup_normal = BeautifulSoup(page_google.text, "html5lib")
    links_normal = soup_normal.findAll("a")
    time.sleep(.600)
    page_google_scholar = requests.get(f"https://scholar.google.com.vn/scholar?q={paper_name}&num={results}")
    soup_scholar = BeautifulSoup(page_google_scholar.text, "html5lib")
    links_scholar = soup_scholar.findAll("a")

    list_links_google = []
    list_links_google_scholar = []
    list_github_links_from_search = []

    # Get all links in GOOGLE and put in list_links_google array
    for link in links_normal :
        link_href = link.get('href')
        if "url?q=" in link_href and not "webcache" in link_href and not "/search%3" in link_href and not "hl%3Dvi" in link_href:
            list_links_google.append(link_href.split("?q=")[1].split("&sa=U")[0])
            # print(link.get('href').split("?q=")[1].split("&sa=U")[0])

    # Get all links in GOOGLE SCHOLAR and put in list_links_google array      
    for link in links_scholar :
        link_href = link.get('href')
        if "https://" in link_href and not "&continue" in link_href and not "?q=cache" in link_href:
            if link_href not in list_links_google:
                list_links_google_scholar.append(link_href)

    # Get all github links in GOOGLE and put in list_github_links_from_search array      
    for link in list_links_google:
        if 'https://github.com' in link:
            list_github_links_from_search.append(link)

    # Get all github links in GOOGLE SCHOLAR and put in list_github_links_from_search array          
    for link in list_links_google_scholar:
        if 'https://github.com' in link:
            list_github_links_from_search.append(link)
    
    return list_links_google, list_links_google_scholar, list_github_links_from_search

# Next step
# Join to top 10 search links and get all texts or links containing "https://github.com"    
def Finding_links(list_links, result):
    i = 0        
    list_github_links_from_link = []
    
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    for link in list_links:  
        link_pwc = []     
        if 'https://github.com' not in link: 
            if 'https://arxiv.org/' not in link and 'https://paperswithcode.com/' not in link:
                if i == 10: break
                else: i=i+1
                print(link)
                try:
                    next_page = requests.get(link, headers=headers, timeout=2)
                    print("join")
                    soup = BeautifulSoup(next_page.content, 'html5lib')
                    output = ''
                    link_a = soup.findAll("a")
                    text = soup.find_all(text=True)
                    for t in text:
                        if t.parent.name not in blacklist:
                            if 'https://github.com' in t:
                                output += t
                    for links in link_a :
                        link_href = links.get('href')
                        if link_href is not None and 'https://github.com' in link_href:
                            list_github_links_from_link.append(link_href)
                    temp_list = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', output)
                    for link in temp_list:
                        if 'https://github.com' in link:
                            list_github_links_from_link.append(link)
                    list_github_links_from_link = list(set(list_github_links_from_link))
                    
                except requests.exceptions.Timeout:
                    print("Timeout occurred")
                except requests.exceptions.ConnectionError:
                    print("Connection Error")
            # 
            elif 'https://arxiv.org/' in link:
                print(link)
                list_git_arxiv, link_pwc = Get_arxiv.get_link_from_arxiv(link)
                result.extend(list_git_arxiv)
                Finding_links(link_pwc, result)
                
            elif 'https://paperswithcode.com/' in link:
                print(link)
                link_git_pwc = Get_pwc.get_link_from_pwc(link)
                result.extend(link_git_pwc)
                         
    return list_github_links_from_link   

