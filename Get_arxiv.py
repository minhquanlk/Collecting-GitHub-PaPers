from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def get_link_from_arxiv(link):
    links_git = []
    link_pwc = []
    
    if 'pdf' not in link:
    
        driver = webdriver.Edge()  
        driver.get(link) 
        print("join")
        driver.find_element_by_css_selector('[for="tabtwo"]').click()
        time.sleep(0.5)
        pwc = driver.find_element_by_id("paperwithcode-toggle")
        pwc.find_element_by_xpath('..').click()
        time.sleep(0.5)
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h3[contains(.,'Official Code')]")))
        except TimeoutException:
            print("Loading took too much time!")
            return links_git, link_pwc

        div_code = driver.find_element_by_id('pwc-output')
        elems = div_code.find_elements_by_tag_name("a")
        if len(elems) != 0:
            for elem in elems:
                links = elem.get_attribute("href")
                if 'https://github.com/' in links:
                    links_git.append(links)
                if 'https://paperswithcode.com/paper/' in links:
                    link_pwc.append(links)
     
    return links_git, link_pwc
