import os
import requests
import pandas as pd
from datetime import datetime

class DataAnalyser:
    def __init__(self, base_api_url):
        self.base_api_url = base_api_url

    def fetch_data(self, start_date, end_date, coin_id):
        # Перетворення дат у datetime об'єкти з часом 00:00:00
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.min.time())

        # Запит даних з API CoinGecko
        params = {
            'vs_currency': 'usd',
            'from': int(start_datetime.timestamp()),
            'to': int(end_datetime.timestamp())
        }
        url = f'{self.base_api_url}/coins/{coin_id}/market_chart/range'
        response = requests.get(url, params=params)
        data = response.json()

        # Перевірка, чи є ключ 'prices' у відповіді
        if 'prices' not in data:
            raise ValueError("Invalid response from API: 'prices' key not found")

        # Перетворення JSON-даних в DataFrame
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        return df

    def save_to_csv(self, data, filename):
        # Перевірка існування директорії data
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Збереження даних у CSV-файл
        filepath = os.path.join('data', filename)
        data.to_csv(filepath)
        return filepath
