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
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

def getcontext(url):
    if("wikipedia" in url): return getcontext_wikipedia(url)
    elif("medium" in url): return getcontext_medium(url)
    elif("geeksforgeeks" in url): return scrape_geekforgeeks_content(url)
    elif("hindustantimes" in url): return scrape_hindustantimes_content(url)
    elif(".pdf" in url): return getcontext_pdf(url)
    else: return "-ERROR-"
    
# PDF FETCH & REQUEST:
def getcontext_pdf(url):
    # url = ":".join(url.split(":")[1:])
    response = requests.get(url)
    open("resource.pdf", "wb").write(response.content)
    
    text = ""
    
    reader = PdfReader("./resource.pdf")
    for page in reader.pages:
        text += page.extract_text()
    
    with open("context.txt", "w+", encoding='utf-8') as file:
        try:
            file.write(text)
            return main_content.text
        except Exception as error:
            file.write('ERROR PARSING PDF: ' + str(error) + '\n')
            
    return True

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

# def scrape_medium_content(url):
#     # Send a GET request to the provided URL
#     URL_Extension = 'http://webcache.googleusercontent.com/search?q=cache:' + url
#     response = requests.get(URL_Extension)

#     if response.status_code == 200:
#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Find the body tag and extract its content
#         # Using find with XPath
#         #xpath_expression = '//*[@id="bN015htcoyT__google-cache-hdr"]/div[2]/span/span[2]/a'
#         specific_id_content = soup.find(id='root').get_text()
#         #element_with_xpath = soup.find('div', {'class': xpath_expression}).get_text()
#         return specific_id_content
    
#     else:
#         print(f"Failed to fetch the page. Status code: {response.status_code}")
#         return None

def scrape_geekforgeeks_content(url):
    # Send a GET request to the provided URL
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the body tag and extract its content
        article_content = soup.find('article').get_text()

        with open("context.txt", "w+", encoding='utf-8') as file:
            try:
                file.write(article_content)
                return article_content
            except Exception as error:
                file.write('ERROR occured: ' + str(error) + '\n')

    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None

def scrape_hindustantimes_content(url):
    # Send a GET request to the provided URL
    URL_Extension = 'http://webcache.googleusercontent.com/search?q=cache:' + url
    response = requests.get(URL_Extension)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the body tag and extract its content
        #specific_class_content = soup.find('div', class_='fullStory tfStory current videoStory story__detail storyAf101700745055757').get_text()
        hindustan_content = soup.find(id='dataHolder').get_text()

        with open("context.txt", "w+", encoding='utf-8') as file:
            try:
                file.write(hindustan_content)
                return hindustan_content
            except Exception as error:
                file.write('ERROR occured: ' + str(error) + '\n')    
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None