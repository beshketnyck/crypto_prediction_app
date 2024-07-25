import requests
import pandas as pd
import datetime

class CryptoAPI:
    def __init__(self, crypto_id='bitcoin'):
        self.crypto_id = crypto_id
        self.base_url = "https://api.coingecko.com/api/v3/simple/price"
        self.history_url = "https://api.coingecko.com/api/v3/coins/{}/history?date={}&localization=false"
        self.trending_url = "https://api.coingecko.com/api/v3/search/trending"

    def get_price(self, currency):
        response = requests.get(f"{self.base_url}?ids={currency}&vs_currencies=usd")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def get_historical_data(self, currency, date):
        response = requests.get(self.history_url.format(currency, date))
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def get_trending_cryptocurrencies(self):
        response = requests.get(self.trending_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
