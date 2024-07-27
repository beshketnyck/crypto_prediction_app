import os
import pandas as pd
import requests
from datetime import datetime, timedelta

class DataAnalyser:
    def __init__(self, base_api_url):
        self.base_api_url = base_api_url

    def fetch_data(self, start_date, end_date, coin_id):
        # Перевірка на часові межі, об'єднання дат для запиту
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        url = f'{self.base_api_url}/coins/{coin_id}/market_chart/range'
        params = {
            'vs_currency': 'usd',
            'from': int(start_datetime.timestamp()),
            'to': int(end_datetime.timestamp())
        }
        
        response = requests.get(url, params=params)
        data = response.json()

        if 'prices' not in data:
            raise ValueError("Invalid response from API: 'prices' key not found")
        
        prices = data['prices']
        market_caps = data.get('market_caps', [])
        volumes = data.get('total_volumes', [])

        # Преобразування JSON-даних у DataFrame
        df_prices = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df_prices['timestamp'] = pd.to_datetime(df_prices['timestamp'], unit='ms')
        df_prices.set_index('timestamp', inplace=True)

        if market_caps:
            df_market_caps = pd.DataFrame(market_caps, columns=['timestamp', 'market_cap'])
            df_market_caps['timestamp'] = pd.to_datetime(df_market_caps['timestamp'], unit='ms')
            df_market_caps.set_index('timestamp', inplace=True)
            df_prices['market_cap'] = df_market_caps['market_cap']

        if volumes:
            df_volumes = pd.DataFrame(volumes, columns=['timestamp', 'volume'])
            df_volumes['timestamp'] = pd.to_datetime(df_volumes['timestamp'], unit='ms')
            df_volumes.set_index('timestamp', inplace=True)
            df_prices['volume'] = df_volumes['volume']

        # Вибірка даних на 12:00 кожного дня
        daily_data = df_prices.resample('D').apply(lambda x: x.at_time('12:00') if '12:00' in x.index.time else x.iloc[0])

        # Переконайтесь, що індекс daily_data має тип datetime.date для порівняння з start_date і end_date
        daily_data.index = daily_data.index.date

        # Фільтрація даних для точного діапазону дат
        daily_data = daily_data[(daily_data.index >= start_date) & (daily_data.index <= end_date)]

        return daily_data

    def save_to_csv(self, df, filename):
        # Збереження даних у CSV
        dir_path = './app/main/data'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        filepath = os.path.join(dir_path, filename)
        df.to_csv(filepath)
        return filepath

    def fetch_twitter_followers(self, coin_id):
        url = f'{self.base_api_url}/coins/{coin_id}'
        response = requests.get(url)
        data = response.json()

        if 'community_data' in data:
            return data['community_data'].get('twitter_followers', 'N/A')
        return 'N/A'
