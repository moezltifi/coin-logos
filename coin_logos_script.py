import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode (no UI)
    chrome_options.add_argument(f'--user-agent={USER_AGENT}')
    
    # Set up ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    return driver

def extract_coin_info(driver, url):
    driver.get(url)
    time.sleep(3)  # Wait for page to load

    # Scroll down to the bottom to trigger lazy loading (loading all 100 coins)
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    # Scroll until we reach the end of the page (to load all coins)
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    coins = []
    coin_elements = driver.find_elements(By.CSS_SELECTOR, 'a.tw-w-full.tw-items-center.tw-w-full')

    for coin in coin_elements:
        try:
            name = coin.find_element(By.CLASS_NAME, 'tw-text-gray-700').text.strip().split('\n')[0]
            symbol = coin.find_element(By.CLASS_NAME, 'tw-block').text.strip()
            logo_link = coin.find_element(By.TAG_NAME, 'img').get_attribute('src').strip()
            if name and symbol and logo_link:
                coins.append({
                    'name': name,
                    'symbol': symbol,
                    'logo_link': logo_link
                })
        except Exception as e:
            print(f"Error extracting coin data: {e}") 
    return coins

def save_to_json(data, file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r+', encoding='utf-8') as json_file:
            try:
                current_data = json.load(json_file)
            except json.JSONDecodeError:
                current_data = []
            current_data.extend(data)
            json_file.seek(0)  
            json.dump(current_data, json_file, ensure_ascii=False, indent=4)
    else:
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

def scrape_page_links(base_url, start_page, end_page):

    return [f"{base_url}{page}" for page in range(start_page, end_page + 1)]

def scrape_coins(base_url, start_page, end_page):
    driver = setup_driver()
    page_urls = scrape_page_links(base_url, start_page, end_page)

    for url in page_urls:
        print(f"Scraping {url}...")
        coins = extract_coin_info(driver, url)
        if coins:
            save_to_json(coins, 'coingecko_coins.json')
        time.sleep(3) 
    
    driver.quit()
    print('Scraping completed and saved to coingecko_coins.json')

if __name__ == "__main__":
    base_url = "https://www.coingecko.com/?page="
    start_page = 1
    end_page = 20  # You can change this as needed for more pages
    scrape_coins(base_url, start_page, end_page)
