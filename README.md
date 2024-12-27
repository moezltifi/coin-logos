# Cryptocurrency Logos Scraper

This project provides cryptocurrency logos for most cryptocurrencies listed on CoinGecko. It scrapes CoinGecko to collect cryptocurrency names, symbols, and their respective logo URLs, saving the data for use in applications or projects. Additionally, the script downloads the logos for offline use.

## Features
- Scrapes cryptocurrency information (name, symbol, and logo URL) from CoinGecko.
- Outputs data in a JSON file.
- Downloads cryptocurrency logos and saves them locally.
- Simple and customizable Python script for updates.

## Prerequisites
- Python 3.7 or higher
- Google Chrome
- The following Python libraries:
  - `selenium`
  - `webdriver-manager`
  - `requests`

Install dependencies using pip:
```bash
pip install selenium webdriver-manager requests
```

## Getting Started

### Clone the Repository
Clone this repository to your local machine:
```bash
git clone <repository_url>
```

### Run the Script
1. Update the `base_url` variable if needed. By default, it scrapes the first 20 pages of CoinGecko:
   ```python
   base_url = "https://www.coingecko.com/?page="
   ```
2. Run the Python script:
   ```bash
   python scrape_coins.py
   ```
3. The script will:
   - Scrape cryptocurrency data from CoinGecko.
   - Save the data in `coingecko_coins.txt`.
   - Download logos into the `logos` folder.

### Customize Pages to Scrape
Modify the `start_page` and `end_page` parameters in the `scrape_coins` function call:
```python
scrape_coins(base_url, start_page=1, end_page=20, output_file="coingecko_coins.txt", logos_folder="logos")
```

## Output
- A JSON file (`coingecko_coins.txt`) containing scraped cryptocurrency data:
  ```json
  {
    "BTC": {
      "name": "Bitcoin",
      "logo_link": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png"
    },
    "ETH": {
      "name": "Ethereum",
      "logo_link": "https://assets.coingecko.com/coins/images/279/large/ethereum.png"
    }
  }
  ```
- A folder (`logos`) containing downloaded logos, named by cryptocurrency symbol (e.g., `BTC.png`).

## Updating Data
To update the data, simply re-run the Python script. The existing `coingecko_coins.txt` file will be overwritten with the latest data, and new logos will be downloaded.

## License
This project is open-source and available under the MIT License.

## Contribution
Feel free to submit issues or pull requests to improve the project.

## Notes
- Ensure you have a stable internet connection while running the script.
- Scraping large amounts of data may take time; adjust the `time.sleep` calls if needed.
- CoinGecko's website structure may change, requiring updates to the script.

## Disclaimer
This project is for educational purposes only. Please use responsibly and adhere to CoinGecko's terms of service.

