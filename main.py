import Get_Google
import Check_github_links

if __name__ == "__main__":
    result = []
    list_github_link = []
    
    search = input("Search: ")
    print('===================================================')
    print('=================== Searching... ==================')
    list_links_google, list_links_google_scholar, list_github_links_from_search = Get_Google.Google_find_links(search)
    list_github_links_from_link = []

    list_github_links_from_link.extend(Get_Google.Finding_links(list_links_google, result))
    list_github_links_from_link.extend(Get_Google.Finding_links(list_links_google_scholar, result))
    
    for link in list_github_links_from_search:
        if link not in result:
            list_github_link.append(link)
            
    for link in list_github_links_from_link:
        if link not in result:
            list_github_link.append(link)
    
    result.extend(Check_github_links.check_link(list_github_link, search)) 
    result = [x.lower() for x in result]
    result = list(set(result))
    
    print('=====================  Done  ======================')
    print('searched ' + str(len(result)) + ' github links for the scientific paper "' + search + '": ')
    print('---')
    if len(result) > 0:
        for link in result:
            print('    ' + link)
    print('---')
    input("Press Enter to exit...")