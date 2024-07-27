import os
import pandas as pd
import requests
from datetime import datetime, timedelta

class DataAnalyser:
    def __init__(self, base_api_url):
        self.base_api_url = base_api_url

    def fetch_data(self, start_date, end_date, coin_id):
        # Перетворення дат на datetime і зміщення часу на один день назад для включення початкової дати
        start_datetime = datetime.combine(start_date, datetime.min.time()) + timedelta(days=1)
        # Зміщення часу на один день вперед для включення кінцевої дати
        end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
        
        params = {
            'vs_currency': 'usd',
            'from': int(start_datetime.timestamp()),
            'to': int(end_datetime.timestamp())
        }
        
        url = f'{self.base_api_url}/coins/{coin_id}/market_chart/range'
        response = requests.get(url, params=params)
        data = response.json()

        if 'prices' not in data:
            raise ValueError("Invalid response from API: 'prices' key not found")

        prices = data['prices']
        market_caps = data.get('market_caps', [])
        volumes = data.get('total_volumes', [])

        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        if market_caps:
            df['market_cap'] = [mc[1] for mc in market_caps]
        else:
            df['market_cap'] = None

        if volumes:
            df['volume'] = [vol[1] for vol in volumes]
        else:
            df['volume'] = None

        # Вибір даних лише за один запис на день
        df = df.resample('D').first()
        
        return df

    def save_to_csv(self, df, filename):
        dir_path = './app/main/data'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        filepath = os.path.join(dir_path, filename)
        df.to_csv(filepath)
        return filepath

    def read_csv(self, filepath):
        return pd.read_csv(filepath, parse_dates=True, index_col='timestamp')
