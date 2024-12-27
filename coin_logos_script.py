import time
import json
import os
import requests
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
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def extract_coin_info(driver, url):
    driver.get(url)
    time.sleep(3)  # Wait for page to load

    # Scroll to the bottom to load all coins
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

    coins = {}
    coin_elements = driver.find_elements(By.CSS_SELECTOR, 'a.tw-w-full.tw-items-center.tw-w-full')

    for coin in coin_elements:
        try:
            name = coin.find_element(By.CSS_SELECTOR, '.tw-text-gray-700.dark\\:tw-text-moon-100.tw-font-semibold.tw-text-sm.tw-leading-5').text.split('\n')[0].strip()
            symbol = coin.find_element(By.CLASS_NAME, 'tw-block').text.strip()
            logo_link = coin.find_element(By.TAG_NAME, 'img').get_attribute('src').strip()
             # Validate data
            if name and symbol and logo_link and logo_link.startswith("https://"):
                coins[symbol] = {'name': name, 'logo_link': logo_link}
            else:
                print(f"Skipped invalid entry: name={name}, symbol={symbol}, logo_link={logo_link}")
        except Exception as e:
            print(f"Error extracting coin data: {e}") 
    return coins

def append_to_file(data, file_name):
    with open(file_name, 'a', encoding='utf-8') as text_file:
        for symbol, details in data.items():
            json_line = f'"{symbol}": {json.dumps(details, ensure_ascii=False)},\n'
            text_file.write(json_line)

def finalize_file(file_name):
    with open(file_name, 'r+', encoding='utf-8') as text_file:
        lines = text_file.readlines()
        # Remove trailing comma from the last entry
        if lines:
            lines[-1] = lines[-1].rstrip(',\n') + '\n'
        text_file.seek(0)
        text_file.write('{\n')
        text_file.writelines(lines)
        text_file.write('}')

def download_logos(file_name, logos_folder):
    if not os.path.exists(logos_folder):
        os.makedirs(logos_folder)

    with open(file_name, 'r', encoding='utf-8') as text_file:
        data = json.loads(text_file.read())

    for symbol, details in data.items():
        logo_url = details['logo_link']
        logo_path = os.path.join(logos_folder, f"{symbol}.png")
        try:
            response = requests.get(logo_url, stream=True)
            if response.status_code == 200:
                with open(logo_path, 'wb') as logo_file:
                    for chunk in response.iter_content(1024):
                        logo_file.write(chunk)
            print(f"Downloaded logo for {symbol}.")
        except Exception as e:
            print(f"Failed to download logo for {symbol}: {e}")

def scrape_coins(base_url, start_page, end_page, output_file, logos_folder):
    driver = setup_driver()

    # Clear the file if it already exists
    if os.path.exists(output_file):
        os.remove(output_file)

    for page in range(start_page, end_page + 1):
        url = f"{base_url}{page}"
        print(f"Scraping {url}...")
        coins = extract_coin_info(driver, url)
        if coins:
            append_to_file(coins, output_file)
        time.sleep(3)

    driver.quit()
    finalize_file(output_file)
    print(f'Scraping completed. Data saved to {output_file}')

    # Download logos
    download_logos(output_file, logos_folder)

if __name__ == "__main__":
    base_url = "https://www.coingecko.com/?page="
    output_file = "coingecko_coins.txt"
    logos_folder = "logos"
    scrape_coins(base_url, start_page=1, end_page=20, output_file=output_file, logos_folder=logos_folder)
