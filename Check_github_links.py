import re
import requests
from bs4 import BeautifulSoup

def num_of_sen(sentence):
    list_word = sentence.split()
    return len(list_word)

def right_links(list_link):
    right_link = []
    for link in list_link:
        match = re.split('/' , link)
        if len(match) == 5:
            right_link.append(link)
    return right_link

def group_words(s, n):
    words = s.split()
    i = 0
    while i < len(s) - n:
        for j in range(i, len(words), n):
            yield ' '.join(words[j:j+n])
        i=i+1
        
def split_search(search):
    dict_key_words = {}
    list_key_words = []
    for i in reversed(range(1,num_of_sen(search) + 1)):
        list_key_words.extend(list(group_words(search, i)))
        list_key_words = list(dict.fromkeys(list_key_words))
    for i in range(1, num_of_sen(search) + 1):
        dict_key_words[i] = []
        for key in list_key_words:
            if num_of_sen(key) == i:
                dict_key_words[i].append(key)
    
    return dict_key_words

def check(search, readme):
    dict_words = split_search(search)
    dict_count = {}
    for i in range(1,len(dict_words)+1):
        dict_count[i] = 0
        for word in dict_words[i]:
            if word in readme:
                dict_count[i] = dict_count[i]+1
        dict_count[i] = dict_count[i]/len(dict_words[i])*100

    percent = dict_count[max(dict_count, key=dict_count.get)]
    
    if percent >= 50:
        return True
    return False

def check_link(list_link, search):
    search = search.replace(": ", " ")
    list_right_link = right_links(list_link)
    result = []
    
    for link in list_right_link:
        print(link)
        git_page = requests.get(link)
        print("join")
        soup = BeautifulSoup(git_page.content, 'html5lib')
        readme = soup.find('article')
        if readme is not None:
            text = readme.find_all(text=True)
            text_in_readme =''
            for t in text:
                text_in_readme += '{} '.format(t)
                
            if check(search, text_in_readme) == True:
                result.append(link)
    
    return result
