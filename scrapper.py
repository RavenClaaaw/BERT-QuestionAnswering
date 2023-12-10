from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
import re
import wikipediaapi

def getcontext(url):
    if("wikipedia" in url): return getcontext_wikipedia(url)
    elif("medium" in url): return getcontext_medium(url)
    else: return "-ERROR-"

def getcontext_wikipedia(url):
    topic = url.split("/")[-1]
    wiki = wikipediaapi.Wikipedia('BERT (merlin@example.com)', 'en')
    page = wiki.page(topic)
    print("Wikipedia Link: ", page.fullurl)
    
    with open("context.txt", "w+", encoding='utf-8') as file:
        try:
            file.write(page.text)
            return page.text
        except Exception as error:
            file.write('ERROR occured: ' + str(error) + '\n')
                
    return page.text
    

def getcontext_medium(site):
    edge_options = Options()
    # search = input("Enter the URL Link: ")
    search = site
    
    # Add the --guest option
    edge_options.add_argument("--guest")

    driver = webdriver.Edge(edge_options)

    driver.get('https://www.clickminded.com/google-cache-search/')

    try:
        search_element = driver.find_element(By.ID, "googlecache")
        search_element.send_keys(search)
        search_element.send_keys(Keys.ENTER)
        time.sleep(5)
    except NoSuchElementException:
        print("Could not find the URL element")

    try: 
        # Get the handles of all open tabs
        all_tabs = driver.window_handles
        # Switch to the second tab
        driver.switch_to.window(all_tabs[1])
    except NoSuchElementException:
        print("Could not find the second tab")

    try:
        text_only_presser = driver.find_element(By.XPATH, '//*[@id="bN015htcoyT__google-cache-hdr"]/div[2]/span/span[2]/a')
        text_only_presser.click()
    except NoSuchElementException:
        print("Could not find the text only element")

    try:
        main_content = driver.find_element(By.ID,'root')
        #main_content = driver.find_element(By.XPATH,'//*[@id="root"]/div')

        # print(main_content.text)
        with open("context.txt", "w+", encoding='utf-8') as file:
            try:
                file.write(main_content.text)
                return main_content.text
            except Exception as error:
                file.write('ERROR occured: ' + str(error) + '\n')


    except NoSuchElementException:
        print("Could not find the main content element")