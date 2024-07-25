import requests
import pandas as pd

class CryptoAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.coingecko.com/api/v3/simple/price"
        self.historical_url = "https://api.coingecko.com/api/v3/coins/{id}/history"

    def get_price(self, currency):
        response = requests.get(f"{self.base_url}?ids={currency}&vs_currencies=usd")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def get_historical_data(self, currency_id, date):
        response = requests.get(self.historical_url.format(id=currency_id), params={"date": date})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def get_market_data(self, currency):
        response = requests.get(f"https://api.coingecko.com/api/v3/coins/{currency}/market_chart", params={"vs_currency": "usd", "days": "1"})
        if response.status_code == 200:
            data = response.json()
            print("Market data fetched:")  # Додано для діагностики
            print(data)  # Додано для діагностики
            prices = data['prices']
            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df.columns = ['timestamp', 'current_price']  # Зміна назви стовпця
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        else:
            print(f"Error: {response.status_code}")
            return None
