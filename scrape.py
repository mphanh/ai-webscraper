# import selenium.webdriver as webdriver
# from selenium.webdriver.chrome.service import Service
# import time
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

AUTH = 'brd-customer-hl_366eb7f6-zone-ai_scraper:h9wyfxclptzi'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape_website(url):
    print("Launching chrome browser...")

    # Use local driver
    # chrome_driver_path = "./chromedriver.exe"
    # options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    # try: 
    #     driver.get(url)
    #     print("Page loaded...")
    #     html = driver.page_source
    #     time.sleep(10)
    #     return html
    # finally:
    #     driver.quit()

    # Use remote driver with brightdata
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(url)
        # CAPTCHA handling
        print("Waiting captcha to solve...")
        solve_res = driver.execute('executeCdpCommand', {
            'cmd': 'Captcha.waitForSolve',
            'params': {
                'detectTimeout': 10000
            }
        })
        print("Captcha solve status:", solve_res['value']['status'])
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html
    
def extract_body_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body()
    if body:
        return str(body)
    return ""

def clean_body_content(body):
    soup = BeautifulSoup(body, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract() # remove script or style tags
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip()) # remove \n that doesn't separate anything
    return cleaned_content
    
def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i:i+max_length] for i in range(0, len(dom_content), max_length)] # split into chunks of max_length; range(begin, end, step)