import requests
import os
from bs4 import BeautifulSoup

class AccessPageError(Exception):
    def __init__(self, e):
        self.e = e

    def __str__(self):
        return f"{self.e.status_code}"

class LoadUserInfoError(Exception):
    def __init__(self):
        pass

    def __str__(self):


class SimpleScraper:

    def __init__(self):
        print("Hello Scraper :)")

    def scrape_fee(self, ticker="EUR_USD"):
        # Start session
        session = requests.Session()

        result = requests.get("https://www.etoro.com/trading/market-hours-fees/?category=crypto-currencies")

        if result.status_code != 200:
            raise FetchPageError(result)

        soup = BeautifulSoup(result.content, 'html.parser')
        target_div = soup.find("div", attrs = {"id": "category_content"} )
        breakpoint()

if __name__ == "__main__":
    scp = SimpleScraper()
    scp.scrape_fee()
